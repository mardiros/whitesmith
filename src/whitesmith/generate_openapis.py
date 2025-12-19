from collections.abc import Sequence
from pathlib import Path
from typing import Any, NewType, get_args

import blacksmith
from blacksmith.domain.registry import HttpResource, registry
from blacksmith.shared_utils.introspection import is_union
from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field, create_model
from pydantic_core import PydanticUndefined

env = Environment(loader=PackageLoader("whitesmith"), autoescape=False)
redoc_template = env.get_template("redoc.jinja2")

sd = blacksmith.SyncRouterDiscovery(
    service_url_fmt="http://{service}.{version}",
    unversioned_service_url_fmt="http://{service}.NaN",
)


HttpStatus = NewType("HttpStatus", str)
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


class OperationResponse(BaseModel):
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
    responses: dict[HttpStatus, OperationResponse]
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


def get_name(typ: type[Any]) -> str:
    schema_name = f"{typ.__module__}__{typ.__qualname__}"
    return schema_name.replace(".", "_")


def request_schema_to_params(
    request: type[blacksmith.Request],
) -> tuple[list[Parameter], RequestBody | None, dict[str, JSONSchema]]:
    if is_union(request):
        args_ = get_args(request)
        allparams: dict[str, Parameter] = {}
        allschemas: dict[str, JSONSchema] = {}
        allschemarefs: dict[str, list[JSONSchema]] = {"oneOf": []}
        union_request_body = RequestBody(
            description=", ".join([argg.__doc__ or argg.__name__ for argg in args_]),
            required=False,
            content=Content.model_validate(
                {
                    # we should read something for the accepted content type
                    "application/json": MediaType(schema=allschemarefs),
                }
            ),
        )
        for argg in args_:
            cparams, creq, cschemas = request_schema_to_params(argg)
            if creq and creq.required:
                union_request_body.required = True
            # fix the override of schema here
            allparams.update({p.name: p for p in cparams})
            allschemas.update(cschemas)
            if content := creq and creq.content:
                if media := content.application_json:
                    if media.schema_ is not None:
                        allschemarefs["oneOf"].append(media.schema_)
        return list(allparams.values()), union_request_body, allschemas

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
        schema_name = get_name(request)
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


def get_schema(
    resp: dict[HttpStatus, OperationResponse], status: HttpStatus
) -> JSONSchema | None:
    if resp.get(status) is None:
        return None
    operresp = resp[status]
    if operresp.content is None:
        return None
    content = operresp.content
    if content.application_json is None:
        return None
    appjson = content.application_json
    return appjson.schema_


def response_schema_to_responses(
    response: type[blacksmith.Response] | None,
) -> tuple[dict[HttpStatus, OperationResponse], dict[str, JSONSchema]]:
    schemas: dict[str, JSONSchema] = {}
    if response and is_union(response):
        all_resp: dict[HttpStatus, OperationResponse] = {}
        all_schema: dict[str, JSONSchema] = {}
        for resp in get_args(response):
            oper_resp, schemas = response_schema_to_responses(resp)
            for key, val in oper_resp.items():
                if key in all_resp:
                    oneOf = []
                    if schema := get_schema(all_resp, key):
                        if schema is not None:
                            if "oneOf" in schema:
                                oneOf = schema["oneOf"]
                            else:
                                oneOf = [schema]

                    if (new_schema := get_schema(oper_resp, key)) is not None:
                        oneOf.append(new_schema)
                    content = Content.model_validate(
                        {
                            "application/json": MediaType.model_validate(
                                {
                                    "schema": {
                                        "oneOf": oneOf,
                                    }
                                }
                            )
                        }
                    )
                    all_resp[key] = OperationResponse(
                        description=f"{all_resp[key].description}, {val.description}",
                        content=content,
                    )

                else:
                    all_resp[key] = val
            all_schema.update(schemas)
        return all_resp, all_schema

    responses: dict[HttpStatus, OperationResponse] = {}
    if response is None:
        responses[HttpStatus("204")] = OperationResponse(description="No Content")
    else:
        schema_name = get_name(response)
        schema_name = schema_name.replace(".", "_")
        responses[HttpStatus("200")] = OperationResponse(
            description=response.__doc__ or response.__name__,
            content=Content.model_validate(
                {
                    # we should read something for the accepted content type
                    "application/json": MediaType.model_validate(
                        {"schema": {"$ref": f"#/components/schemas/{schema_name}"}}
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
            parameters, req_body, req_schemas = request_schema_to_params(schemas[0])
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
