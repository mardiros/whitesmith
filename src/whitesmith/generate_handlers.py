from pathlib import Path
from typing import Any, List, Optional, Sequence, Set

import blacksmith
from blacksmith.domain.registry import HttpResource, registry
from jinja2 import Environment, PackageLoader
from pydantic import BaseModel, Field

env = Environment(loader=PackageLoader("whitesmith"), autoescape=False)
handlers_template = env.get_template("handlers.jinja2")
conftest_template = env.get_template("conftest.jinja2")
fixtures_template = env.get_template("fixtures.jinja2")

sd = blacksmith.SyncRouterDiscovery(
    service_url_fmt="http://{service}.{version}",
    unversioned_service_url_fmt="http://{service}.NaN",
)

cli: blacksmith.SyncClientFactory[Any, Any] = blacksmith.SyncClientFactory(sd=sd)


class ResponseModel(BaseModel):
    mod: str = Field(...)
    name: str = Field(...)

    def __hash__(self) -> int:
        return hash(f"{self.mod}:{self.name}")


class Route(BaseModel):
    python_method: str = Field(...)
    http_method: str = Field(...)
    url_pattern: str = Field(...)
    response_model: str = Field(...)


class HandlerTemplateContext(BaseModel):
    response_models: Set[ResponseModel] = Field(default_factory=set)
    routes: List[Route] = Field(default_factory=list)

    def add_resource(
        self,
        endpoint: str,
        service: str,
        name: str,
        resource: Optional[HttpResource],
        prefix: str = "",
    ) -> "HandlerTemplateContext":

        if not resource or not resource.contract:
            return self
        for method, schemas in resource.contract.items():
            response_schema = schemas[1]
            response_schema_name = ""
            if response_schema:
                response_schema_name = response_schema.__name__
                self.response_models.add(
                    ResponseModel(
                        mod=response_schema.__module__,
                        name=response_schema.__name__,
                    )
                )

            self.routes.append(
                Route(
                    python_method=f"{service}_{name}_{prefix}{method}".lower(),
                    http_method=f"{method}",
                    url_pattern=f"{endpoint}{resource.path}",
                    response_model=response_schema_name,
                )
            )
        return self


def generate_handlers(
    outdir: Path, resources_mod: Sequence[str], overwrite: bool
) -> None:

    blacksmith.scan(*resources_mod)

    print("Generating mocks from blacksmith registry...")

    outdir = outdir / "whitesmith"
    for client, service in registry.client_service.items():

        service, resources = registry.get_service(client)
        endpoint = sd.get_endpoint(*service)

        print(f"Processing client {client}...")

        context = HandlerTemplateContext()
        for name, resource in resources.items():
            context = context.add_resource(
                endpoint, client, name, resource.collection, prefix="collection_"
            ).add_resource(endpoint, client, name, resource.resource)

        outdir.mkdir(exist_ok=True)
        file_ = outdir / "__init__.py"
        if overwrite or not (outdir / "__init__.py").exists():
            print(f"Writing {file_}")
            file_.write_text("")

        file_ = outdir / "conftest.py"
        if overwrite or not file_.exists():
            conftest = conftest_template.render()
            print(f"Writing {file_}")
            file_.write_text(conftest)

        file_ = outdir / "fixtures.py"
        if overwrite or not file_.exists():
            conftest = fixtures_template.render(context={"resources": resources_mod})
            print(f"Writing {file_}")
            file_.write_text(conftest)

        (outdir / "handlers").mkdir(exist_ok=True)

        file_ = outdir / "handlers" / "__init__.py"
        if overwrite or not file_.exists():
            print(f"Writing {file_}")
            file_.write_text("")

        file_ = outdir / "handlers" / f"{client}.py"
        if overwrite or not file_.exists():
            print(f"Writing {file_}")
            handler = handlers_template.render(context=context)
            file_.write_text(handler)
