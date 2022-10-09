from typing import Optional
import blacksmith
from blacksmith.domain.registry import registry, HttpResource

sd = blacksmith.SyncRouterDiscovery(
    service_url_fmt="http://{service}.{version}",
    unversioned_service_url_fmt="http://{service}.NaN",
)

cli = blacksmith.SyncClientFactory(sd=sd)



def gen_contracts(endpoint: str, resource: Optional[HttpResource]):
    if not resource or not resource.contract:
        return
    for method, schemas in resource.contract.items():
        print(f"{method} {endpoint}{resource.path}")
        print(schemas)


def main():
    print("Generating mocks from blacksmith registry...")
    blacksmith.scan("tests.resources")
    print(registry.clients)
    print(registry.client_service)
    for client, service in registry.client_service.items():
        endpoint = sd.get_endpoint(*service)
        service, resources = registry.get_service(client)

        print ()
        print (f"Processing {client}")
        print ()

        for name, resource in resources.items():
            gen_contracts(endpoint, resource.resource)
            gen_contracts(endpoint, resource.collection)
