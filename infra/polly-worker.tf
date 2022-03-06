terraform {
  required_providers {
    docker = {
      source = "terraform-providers/docker"
      version = "~> 2.3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "audio-notion-polly-worker" {
  name         = "naboagye1/audio-notion-polly-worker:latest"
  keep_locally = false
}

resource "docker_container" "an-polly-worker" {
  image = docker_image.audio-notion-polly-worker.latest
  name  = "an-polly-worker"
  ports {
    internal = 3080
    external = 8080
  }
}