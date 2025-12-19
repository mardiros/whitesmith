from collections.abc import Sequence
from pathlib import Path
from typing import Any

import blacksmith
from blacksmith.domain.registry import HttpResource, registry
from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field, create_model
from pydantic_core import PydanticUndefined

env = Environment(loader=PackageLoader("whitesmith"), autoescape=False)
redoc_template = env.get_template("redoc.jinja2")

sd = blacksmith.SyncRouterDiscovery(
    service_url_fmt="http://{service}.{version}",
    unversioned_service_url_fmt="http://{service}.NaN",
)


JSONSchema = dict[str, Any]


class Parameter(BaseModel):
    name: str
    in_: str = Field(alias="in")  # path, query, header
    required: bool = Field(default=False)
    schema_: JSONSchema | None = Field(alias="schema", default=None)


class MediaType(BaseModel):
    schema_: JSONSchema | None = Field(alias="schema", default=None)


class Content(BaseModel):
    application_json: MediaType | None = Field(default=None, alias="application/json")


class Response(BaseModel):
    description: str = Field(default="OK")
    content: Content | None = Field(default=None)


class RequestBody(BaseModel):
    description: str | None = Field(default=None)
    required: bool = Field(default=False)
    content: Content | None = Field(default=None)


class Operation(BaseModel):
    operationId: str
    summary: str
    parameters: list[Parameter] = Field(default_factory=list)
    responses: dict[str, Response]
    requestBody: RequestBody | None = (
        None  # Optional, for POST/PUT bodies    summary: str
    )
    tags: list[str]


class Components(BaseModel):
    schemas: dict[str, JSONSchema] = Field(default_factory=dict)


class Info(BaseModel):
    title: str
    version: str


class Server(BaseModel):
    url: str
    description: str | None = None


class OpenAPIDocument(BaseModel):
    openapi: str = "3.1.0"
    info: Info
    paths: dict[str, dict[str, Operation]] = Field(default_factory=dict)
    components: Components = Field(default_factory=Components)
    servers: list[Server] = Field(default_factory=list)


def request_schema_to_parameter(
    request: type[blacksmith.Request],
) -> tuple[list[Parameter], RequestBody | None, dict[str, JSONSchema]]:
    params: list[Parameter] = []
    json_schemas = request.model_json_schema()
    postbody_required = False
    postbody: dict[str, Any] = {}
    for name, field in request.model_fields.items():
        match field.json_schema_extra["location"]:  # type: ignore
            case "querystring" | "headers" | "path":
                param = Parameter.model_validate(
                    {
                        "name": field.alias or name,
                        "in": field.json_schema_extra["location"],  # type: ignore
                        "required": field.is_required(),
                        "schema": json_schemas["properties"][name],
                    }
                )
                params.append(param)
            case "body":
                field_type = field.annotation
                if field.default is not PydanticUndefined:
                    postbody[name] = (field_type, field.default)
                elif field.default_factory is not None:
                    postbody[name] = (field_type, field.default_factory)
                else:
                    postbody[name] = field_type
                postbody_required = postbody_required or field.is_required()
            case _:
                # what to do with attachement
                pass
    schemas = {}
    request_body: RequestBody | None = None
    if postbody:
        schema_name = f"{request.__qualname__}RequestBody"
        model = create_model(schema_name, **postbody)  # type: ignore
        schemas[schema_name] = model.model_json_schema()
        request_body = RequestBody(
            description=request.__doc__ or request.__qualname__,
            required=postbody_required,
            content=Content.model_validate(
                {
                    # we should read something for the accepted content type
                    "application/json": MediaType(
                        schema={"$ref": f"#/components/schemas/{schema_name}"}
                    ),
                }
            ),
        )
    return params, request_body, schemas


def response_schema_to_responses(
    response: type[blacksmith.Response] | None,
) -> tuple[dict[str, Response], dict[str, JSONSchema]]:
    schemas: dict[str, JSONSchema] = {}
    responses: dict[str, Response] = {}
    if response is None:
        responses["204"] = Response(description="No Content")
    else:
        schema_name = f"{response.__module__}__{response.__qualname__}"
        schema_name = schema_name.replace(".", "_")
        responses["200"] = Response(
            description=response.__doc__ or response.__name__,
            content=Content.model_validate(
                {
                    # we should read something for the accepted content type
                    "application/json": MediaType(
                        schema={"$ref": f"#/components/schemas/{schema_name}"}
                    ),
                }
            ),
        )
        schemas[schema_name] = response.model_json_schema()

    return responses, schemas


def add_resource(
    openapi: OpenAPIDocument,
    resource: HttpResource,
    client: str,
    resource_name: str,
    summary: str,
    tags: list[str],
) -> None:
    if resource.contract:
        for http_method, schemas in resource.contract.items():
            method = http_method.lower()
            parameters, req_body, req_schemas = request_schema_to_parameter(schemas[0])
            openapi.components.schemas.update(req_schemas)
            responses, resp_schemas = response_schema_to_responses(schemas[1])
            openapi.components.schemas.update(resp_schemas)
            if resource.path not in openapi.paths:
                openapi.paths[resource.path] = {}
            openapi.paths[resource.path][method] = Operation(
                operationId=f"{client}_{method}_{resource_name}",
                summary=summary,
                parameters=parameters,
                requestBody=req_body,
                responses=responses,
                tags=tags,
            )


def generate_openapis(
    outdir: str | Path, resources_mod: Sequence[str], overwrite: bool
) -> None:
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    blacksmith.scan(*resources_mod)

    print("Generating openapis from blacksmith registry...")

    services = []
    for client, service in registry.client_service.items():
        service, resources = registry.get_service(client)
        endpoint = sd.get_endpoint(*service)

        print(f"Processing client {client}...")
        openapi = OpenAPIDocument(
            info=Info(
                title=f"{client} for service {service[0]}",
                version=service[1] or "unversionned",
            ),
            servers=[
                Server(
                    url=endpoint,
                    description="Client Contract Testing",
                )
            ],
        )
        for name, resource in resources.items():
            print(f"Prosessing {name}...")
            if resource.collection:
                add_resource(
                    openapi,
                    resource.collection,
                    client,
                    f"{name}_collection",
                    summary=f"Collection or {name}",
                    tags=[name],
                )

            if resource.resource:
                add_resource(
                    openapi, resource.resource, client, name, summary=name, tags=[name]
                )

        file_ = outdir / f"{client}.json"
        services.append(
            {
                "file": f"/{client}.json",
                "name": client,
                "id": client.replace(" ", "-"),
                "endpoint": endpoint,
            }
        )
        if overwrite or not file_.exists():
            print(f"Writing {file_}")
            file_.write_text(openapi.model_dump_json(by_alias=True, exclude_none=True))

    file_ = outdir / "index.html"
    if overwrite or not file_.exists():
        print(f"Writing {file_}")
        redoc = redoc_template.render(
            services=services,
        )
        file_.write_text(redoc)
