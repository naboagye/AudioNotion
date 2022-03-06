terraform {
  required_providers {
    docker = {
      source = "terraform-providers/docker"
      version = "~> 2.3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "audio-notion" {
  name         = "naboagye1/audio-notion:latest"
  keep_locally = false
}

resource "docker_container" "an-frontend" {
  image = docker_image.audio-notion.latest
  name  = "audio-notion-frontend"
  ports {
    internal = 3080
    external = 8080
  }
}