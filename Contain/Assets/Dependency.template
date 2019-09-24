import Contain

class {class_name}Dependency: BaseDependency, Injecting {

    lazy var {property_name}: {class_name} = { return {class_name}(container: self.container) }()

    override func inject(into consumer: AnyObject) {
        guard let consumer = consumer as? {class_name}Consumer else {
            return
        }
        consumer.{property_name} = {property_name}
    }
}
