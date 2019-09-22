//  Created by Axel Ancona Esselmann on 9/22/19.
//  Copyright © 2019 Axel Ancona Esselmann. All rights reserved.
//

#if os(iOS)
import UIKit

public protocol AppDelegateConsumer: class {
    var appDelegate: UIApplicationDelegate? { get set }
}

public class AppDelegateDependency: Dependency {

    public required init(container: ContainerProtocol) { fatalError("Not needed") }

    weak var appDelegate: UIApplicationDelegate?

    public init(appDelegate: UIApplicationDelegate) {
        self.appDelegate = appDelegate
    }

    public func inject(into consumer: AnyObject) {
        guard let consumer = consumer as? AppDelegateConsumer else {
            return
        }
        guard let appDelegate = appDelegate else {
            return
        }
        consumer.appDelegate = appDelegate
    }
}
#endif
