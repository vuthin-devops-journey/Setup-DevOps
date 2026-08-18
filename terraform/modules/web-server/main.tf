data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023*-x86_64"]
  }
}

data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "this" {
  name        = "${var.name}-sg"
  description = "Managed by web-server module"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "this" {
  ami                    = data.aws_ami.al2023.id
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.this.id]

  user_data = <<-USERDATA
    #!/bin/bash
    dnf install -y docker
    systemctl enable --now docker
    docker run -d -p 80:5000 --restart always ${var.container_image}
  USERDATA

  tags = {
    Name = "${var.name}-server"
  }
}
