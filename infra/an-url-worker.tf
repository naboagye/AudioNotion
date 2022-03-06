terraform {
  required_providers {
    docker = {
      source = "terraform-providers/docker"
      version = "~> 2.3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "audio-notion-url-worker" {
  name         = "naboagye1/audio-notion-url-worker:latest"
  keep_locally = false
}

resource "docker_container" "an-url-worker" {
  image = docker_image.audio-notion-url-worker.latest
  name  = "an-url-worker"
  ports {
    internal = 3080
    external = 8080
  }
}