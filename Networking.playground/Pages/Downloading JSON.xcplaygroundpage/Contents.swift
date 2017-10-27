import Foundation
import PlaygroundSupport

//: [Previous](@previous)

/*:
 # Downloading JSON
 
 More often than not, we will be dealing with JSON responses from servers.
 Lets look at how we will grab some json from an API using a *get* request.
 
 ## JSON
 
 JSON stands for Javascript Object Notation.
 It is one of a few formats that is used to transfer information over the web.
 JSON looks like this:
 {
 "name": "Eliel"
 "age": 23
 }
 
*/

let url = URL(string: "https://jsonplaceholder.typicode.com/photos/1")!

var request = URLRequest(url: url)
request.httpMethod = "GET"

let session = URLSession.shared

let task = session.dataTask(with: request) { (data, response, error) in
    
    if let data = data {
        let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments)
        let dictionary = json as? [String:Any]
        let title = dictionary!["title"]
        print(title ?? "Empty")
    }
}

// Don't forget to resume task
task.resume()


/*:
 ## Sessions
 
 There are three main session types:
 1. session.uploadTask   :- Used for uploading binary files
 2. session.downloadTask :- Used for downloading binary files
 3. session.dataTask     :- Used for uploading and downloading and deleting text/html/json
 
 
 */

/*:
 ## Uploading JSON data
 
 We often need to upload data to our servers.
 Imagine creating a new user account for an app, we would need to upload information about the user necessary to create the account.
 */

/*:
 JSON in Swift is represented as a dictionary with a String key to an Any type as the value
 
 Why is that so? Lets take a look at the structure of a JSON Object.
 {
 "user": {
 "age": 23,
 "name": "peter",
 "location": [27.33, -122]
 }
 }
 
 From the above example we can see that the keys are always Strings and the values can be *Any* type of object(Int, String, Array, another JSON Object).
 
 */

//: ### Uploading JSON data
//: Lets define our JSON type as a dictionary of String to Any
typealias JSON = [String: Any]

//URL/url parameters
var postReq = URLRequest(url: URL(string: "https://httpbin.org/post")!)

//will be Body
let jsonDictionary: JSON = ["user": ["first_name": "Eliel", "last_name": "Gordon"]]
let jsonData = try? JSONSerialization.data(withJSONObject: jsonDictionary, options: JSONSerialization.WritingOptions.prettyPrinted)

//Method
postReq.httpMethod = "POST"
//Body
postReq.httpBody = jsonData

//session.dataTask(with: postReq) { (data, resp, err) in
//    if let data = data {
//        let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments)
//        print(json ?? "")
//    }
//}.resume()


/*:
 ## Challenges

 1. Can you think of a type safe way to wrap the http methods of a request?
 2. Find some JSON API resources online and use URLSession to download the JSON

*/
enum Method: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case delete = "DELETE"
}

let pokeUrl = URL(string: "http://pokeapi.co/api/v2/language/6")!

var pokeRequest = URLRequest(url: pokeUrl)
pokeRequest.httpMethod = Method.get.rawValue

let pokeSession = URLSession.shared

let pokeTask = pokeSession.dataTask(with: pokeRequest) { (data, response, error) in
    if let data = data {
        guard let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments) else {return}
        let dictionary = json as? [String : Any]
        // Get array of dictionaries
        let namesArray = dictionary!["names"] as? [[String:Any]]
        // Get first object of array and get the name key:value
        let nameIndex = namesArray![0]["name"]
        print(nameIndex ?? "empty")
    }
}


pokeTask.resume()

let spaceXUrl = URL(string: "https://api.spacexdata.com/v1/vehicles/dragon")!

var spaceXRequest = URLRequest(url: spaceXUrl)
spaceXRequest.httpMethod = Method.get.rawValue

let spaceXSession = URLSession.shared

let spaceXTask = spaceXSession.dataTask(with: spaceXRequest) { (data, response, error) in
    if let data = data {
        guard let json = try? JSONSerialization.jsonObject(with: data, options: .allowFragments) else {return}
//        print(json)
        let dictionary = json as? [String : Any]
        // Get the name key:value
        let name = dictionary!["name"]
        print(name ?? "empty")
        let variations = dictionary!["variations"] as? [String:Any]
        let cargo = variations!["cargo"] as? [String:Any]
        let details = cargo!["details"]
        print(details ?? "empty")
//        // Get first object of array and get the name key:value
//        let nameIndex = namesArray![0]["name"]
//        print(nameIndex ?? "empty")
    }
}


spaceXTask.resume()

/*: ## Resources
 [URLSessions](https://www.raywenderlich.com/158106/urlsession-tutorial-getting-started)
 */

//: Below is code required to run this playground, it is not a part of the class material
PlaygroundSupport.PlaygroundPage.current.needsIndefiniteExecution = true

//: [Next](@next)
