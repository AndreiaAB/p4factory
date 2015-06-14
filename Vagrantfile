
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "ubuntu/trusty64"

    config.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
        v.customize ["modifyvm", :id, "--cpus", "2"]
        v.customize ["modifyvm", :id, "--memory", "2048"]
    end

    config.ssh.forward_x11 = true

    config.vm.provision "shell", privileged: false, path: "./install.sh"
    config.vm.provision "shell", privileged: false, inline: "ln -s /vagrant p4factory"
end
