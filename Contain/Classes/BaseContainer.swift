//  Created by Axel Ancona Esselmann on 9/22/19.
//  Copyright © 2019 Axel Ancona Esselmann. All rights reserved.
//

import Foundation

public typealias Dependency = Injectable & Injecting

public protocol Injecting {
    func inject(into consumer: AnyObject)
}

open class BaseDependency: Injectable {
    public let container: ContainerProtocol // retain cycle?

    public required init(container: ContainerProtocol) {
        self.container = container
    }

    open func inject(into consumer: AnyObject) {
        propertyInjection()
    }

    open func propertyInjection() { }
}

open class BaseContainer: ContainerProtocol {

    open func dependencyTypes() -> [Dependency.Type] {
        return []
    }

    open func codeGenDependencyTypes() -> [Dependency.Type] {
        return []
    }

    private var dependencies: [Dependency]

    public init(_ outsideDependencies: Dependency...) {
        dependencies = outsideDependencies
        let types = dependencyTypes() + codeGenDependencyTypes()
        dependencies += types.compactMap { [weak self] type in
            guard let strongSelf = self else {
                return nil
            }
            return type.init(container: strongSelf)
        }
    }

    open func inject(_ consumer: AnyObject) {
        for dependency in dependencies {
            dependency.inject(into: consumer)
        }
    }
}
