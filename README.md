# Contain

## Installation

Contain is available through [CocoaPods](https://cocoapods.org). To install
it, simply add the following line to your Podfile:

```ruby
pod 'Contain'
```

- Add a Run Script build phase that executes
```ruby
"${PODS_ROOT}/Contain/Contain/Assets/add_dependencies_to_container.py" "$PROJECT_DIR/${TARGET_NAME}"
```

To create a new dependency add a consumer in `Consumers.swift`:
```ruby
protocol MyClassConsumer: class {
    var myClass: MyClass? { get set }
}
```

`MyClass` either needs to inherit from `BaseInjectable` or adhere to the `Injectable` protocol.
Note: When adhering to `Injectable` make sure to follow the constructor pattern used in `BaseInjectable`.

## Author

anconaesselmann, axel@anconaesselmann.com

## License

Contain is available under the MIT license. See the LICENSE file for more info.
