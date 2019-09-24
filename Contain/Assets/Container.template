import Contain

class Container: BaseContainer {

    init(appDelegate: AppDelegate) {
        let appDelegateDependency = AppDelegateDependency(appDelegate: appDelegate)
        super.init(appDelegateDependency)
        inject(appDelegate)
    }

    /// Do not modify this method!
    override func codeGenDependencyTypes() -> [Dependency.Type] {
		return [
		]
    }

}
