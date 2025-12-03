# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
    config.ssh.insert_key = false
    config.vbguest.auto_update = false
    config.ssh.forward_x11 = true

    # --- Maquina Emissora ---
    config.vm.define "sender" do |sender|
        sender.vm.box = "ubuntu/trusty64"
        sender.vm.hostname = "sender"
        sender.vm.network "private_network", ip: "192.168.56.20"
        sender.vm.synced_folder "src", "/home/vagrant/src"
        sender.vm.provider "virtualbox" do |vb|
            vb.name = "SelectiveRepeat-Sender"
            opts = ["modifyvm", :id, "--natdnshostresolver1", "on"]
            vb.memory = "256"
        end
        sender.vm.provision "shell", path: "bootstrap-client.sh"
    end

    # --- Maquina Receptora ---
    config.vm.define "receiver" do |receiver|
        receiver.vm.box = "ubuntu/trusty64"
        receiver.vm.hostname = "receiver"
        receiver.vm.network "private_network", ip: "192.168.56.21"
        receiver.vm.synced_folder "src", "/home/vagrant/src"
        receiver.vm.provider "virtualbox" do |vb|
            vb.name = "SelectiveRepeat-Receiver"
            opts = ["modifyvm", :id, "--natdnshostresolver1", "on"]
            vb.memory = "256"
        end
        receiver.vm.provision "shell", path: "bootstrap-client.sh"
    end
end
