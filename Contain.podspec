#
# Be sure to run `pod lib lint Contain.podspec' to ensure this is a
# valid spec before submitting.
#
# Any lines starting with a # are optional, but their use is encouraged
# To learn more about a Podspec see https://guides.cocoapods.org/syntax/podspec.html
#

Pod::Spec.new do |s|
  s.name             = 'Contain'
  s.version          = '0.1.0'
  s.summary          = 'Dependency injection container.'
  s.swift_version    = '5.0'


  s.description      = <<-DESC
Experimental dependency injection container.
                       DESC

  s.homepage         = 'https://github.com/anconaesselmann/Contain'
  # s.screenshots     = 'www.example.com/screenshots_1', 'www.example.com/screenshots_2'
  s.license          = { :type => 'MIT', :file => 'LICENSE' }
  s.author           = { 'anconaesselmann' => 'axel@anconaesselmann.com' }
  s.source           = { :git => 'https://github.com/anconaesselmann/Contain.git', :tag => s.version.to_s }

  s.ios.deployment_target = '10.0'
  s.watchos.deployment_target = '3.0'

  s.source_files = 'Contain/Classes/**/*'

  # s.resource_bundles = {
  #   'Contain' => ['Contain/Assets/*.png']
  # }

  s.script_phases = [
    { :name => 'Add dependencies to container',
      :script => 'python "${PODS_TARGET_SRCROOT}/add_dependencies_to_container.py" "$PROJECT_DIR"',
      :execution_position => :before_compile
    }
  ]
end
