# create temp dir
mkdir -p tmp


# openapi-python-client generate --path openapi.json --output-path src/openapi
# copy the files into tmp dir

openapi-generator-cli generate -i openapi.json -g python -o tmp  --skip-validate-spec

# copy from tmp/freestyle_sandboxes_client to src/openapi
rm -rf src/openapi
cp -r tmp/openapi_client src/_openapi_client

# rename everything from openapi_client to _openapi_client in the generated code
find src/_openapi_client -type f -exec sed -i '' 's|openapi_client|_openapi_client|g' {} \;


# delete tmp dir
rm -rf tmp
