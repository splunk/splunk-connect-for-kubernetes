require 'fileutils'
require 'yaml'

release_name = 'RELEASE-NAME'
@version = File.read('VERSION').strip
name_prefix = "#{release_name}-splunk-kubernetes-"

def sanitize_yaml(yaml)
  yaml = YAML.load(yaml)
  %w[chart release heritage].each { |label|
    yaml['metadata']['labels'].delete label

    spec = yaml.fetch('spec', {})
    spec.fetch('selector', {}).fetch('matchLabels', {}).delete(label)
    spec.fetch('template', {}).fetch('metadata', {}).fetch('labels', {}).delete(label)
  }

  %w[checksum/config checksum/helpers].each { |a|
    yaml.fetch('spec', {}).fetch('template', {}).fetch('metadata', {}).fetch('annotations', {}).delete(a)
  }

  yaml['metadata']['labels']['version'] = @version
  yaml.fetch('spec', {}).tap { |spec|
    spec.fetch('selector', {}).fetch('matchLabels', {})['version'] = @version
    spec.fetch('template', {}).fetch('metadata', {}).fetch('labels', {})['version'] = @version
  }

  YAML.dump yaml
end

def write_file
  return unless @file
  puts "Create file #@file"
  open(@file, 'w') { |f| f << sanitize_yaml(@buffer.join) }
  @file = nil
end

while $stdin.gets()
  if $_ =~ /^---\s*$/
    write_file
    next
  end

  if $_ =~ %r'^# Source: .*/([^/]+)/(?:[^/]+)/([^/]+\.yaml)$' && !@file
    FileUtils.mkdir_p File.join(ARGV[0] || '.', $1)
    @file = File.join ARGV[0] || '.', $1, $2
    @buffer = []
    next
  end

  next unless @buffer

  @buffer << $_.sub(name_prefix, "splunk-kubernetes-")
end

write_file
