# Contain

### Contain is a lightweight dependency injection framework for IOS projects. It is written is swift.

## Installation

Contain is available through [CocoaPods](https://cocoapods.org). To install
it, simply add the following line to your Podfile:

```ruby
pod 'Contain'
```

## How to use Contain

Create a container instance inside your AppDelegate:
```ruby
import UIKit
import Contain

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?
    var container: ContainerProtocol?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        container = Container(appDelegate: self)
        return true
    }
}
```

When working without storyboards inject the container into the root view controller and pass it along from there.


When working with storyboards, access the container on the `AppDelegate` inside the application's first screen:

```ruby
guard let container = (UIApplication.shared.delegate as? AppDelegate)?.container else {
    return
}
```
and pass it along from there.


To create a new dependency add a consumer in `Consumers.swift`:
```ruby
protocol MyClassConsumer: class {
    var myClass: MyClass? { get set }
}
```

`MyClass` either needs to inherit from `BaseInjectable` or adhere to the `Injectable` protocol.
Note: When adhering to `Injectable` make sure to follow the constructor pattern used in `BaseInjectable`.


Any consumer of a dependency just has to inherit from `BaseInjectable` or adhere to the `Injectable` protocol and adhere to the desired `Consumer` protocol.


Example for `MyClassConsumer`:

```ruby
class MyClass: BaseInjectable {

}

class MyViewModel: BaseInjectable, MyClassConsumer {
    var myClass: MyClass?
}
```

`MyViewModel` can now be injected with the container, and `myClass` will get assigned inside `MyViewModel`'s initializer.


If the container was injected into the view controller's initializer, view models can be initialized as follows:

```ruby
lazy var viewModel: { MyViewModel(container: container) }()
```


## Author

anconaesselmann, axel@anconaesselmann.com

## License

Contain is available under the MIT license. See the LICENSE file for more info.
