nodes = [
  {
    :hostname => 'axe',
    :ram => 2048,
    :ip => '192.168.56.1',
    #:cpu_cap => 50,
    :cpu => 2,
    :gui => false,
    :box => 'debian/stretch64',
    :bash_provision => 'vagrant/bootstrap.sh',
  },
]


Vagrant.configure("2") do |config|
  nodes.each do |node|
    config.vm.define node[:hostname] do |nodeconfig|
      nodeconfig.vm.synced_folder ".", "/vagrant", type: "virtualbox"

      if node.key?(:ansible_provision)
        nodeconfig.vm.provision "ansible" do |ansible|
          ansible.playbook = node[:ansible_provision]
        end
      end
      if node.key?(:bash_provision)
        nodeconfig.vm.provision :shell, path: node[:bash_provision]
      end
      if node.key?(:box_version)
        nodeconfig.vm.box_version = node[:box_version]
      end
      nodeconfig.vm.box = node[:box]
      nodeconfig.vm.hostname = node[:hostname] + ".box"
      nodeconfig.vm.network :private_network, ip: node[:ip]

      memory = node[:ram] ? node[:ram] : 1048;
      cpu_cap = node[:cpu_cap] ? node[:cpu_cap] : 50;

      nodeconfig.vm.provider :virtualbox do |vb|
        vb.gui = node.fetch(:gui, false)
        vb.customize [
          "modifyvm", :id,
          "--cpuexecutioncap", cpu_cap.to_s,
          "--memory", memory.to_s,
          "--cpus", node.fetch(:cpu, 1),
        ]
      end
    end
  end
end