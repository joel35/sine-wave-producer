registry := ghcr.io/graham-tek
image_name := sine-wave-producer
latest_tag := latest
version_tag := 0.4.0


publish: Dockerfile
	$(info Make: Build $(image_name):$(version_tag) & push to $(registry))
	docker buildx build \
		--platform linux/arm64,linux/amd64 \
		--tag $(registry)/$(image_name):$(latest_tag) \
		--tag $(registry)/$(image_name):$(version_tag) \
		--push \
		.

build_local: Dockerfile
	$(info Make: Build $(image_name) & push to local registry)
	docker build \
		--tag local/$(image_name):$(latest_tag) \
		--tag local/$(image_name):$(version_tag) \
		.
