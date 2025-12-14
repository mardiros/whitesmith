## 5.1.0 - Released on 2025-12-14
* Add a new subcommand whitesmith generate-openapi that generate
  open api json files and html based on redoc. 

## 5.0.1 - Released on 2025-12-13
* Hotfix whitesmith router fixture for nested tests.

## 5.0.0 - Released on 2025-12-13
* Upgrade to blacksmith 5.0
* Rewrite the package in order to expose pytest fixtures directly.
  The API is more clean from a user perspective.

## 4.0.2 - Released on 2025-02-18
* Update generation from template using new router method (get, post, ...)
* Improve test coverage

## 4.0.1 - Released on 2024-12-06
* Remove deprecation warning

## 4.0.0 - Released on 2024-11-03
* Use blacksmith 4
* Drop python 3.8 support
* Update code license to MIT
* Update packaging to use uv/pdm
* Update CI

## 0.6.0 - Released on 2024-06-26
* Use blacksmith 3
* Drop python 3.7 support

## 0.5.0 - Released on 2024-01-20
* Replace pydantic-factories by polyfactory for python >=3.8
  The condition to detect the version of pydantic is not ideal
  and should be updated on a next patch version.

## 0.4.0 - Released on 2023-12-01
* Add method router.get, router.post and so on to get more readable routes

## 0.3.1 - Released on 2023-03-15
* Fix typing

## 0.3.0 - Released on 2023-03-15
* Implement collection_get response

## 0.2.0 - Released on 2022-10-11
* Bump to blacksmith 2.0

## 0.1.3 - Released on 2022-10-10
* Fix typing issue on generated modules

## 0.1.2 - Released on 2022-10-09
* Add missing py.typed marker

## 0.1.1 - Released on 2022-10-09
* Downgrade compatibility to python 3.7
* Add licence

## 0.1.0 - Released on 2022-10-09
* Initial Release
