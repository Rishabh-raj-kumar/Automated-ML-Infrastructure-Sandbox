resource "kind_cluster" "ml_sandbox" {
  name           = "ml-sandbox-cluster"
  node_image     = "kindest/node:v1.30.0" # ARM64 compatible image
  wait_for_ready = true

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = "control-plane"
    }

    node {
      role = "worker"
    }
  }
}