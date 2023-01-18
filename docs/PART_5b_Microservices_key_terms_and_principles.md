# Key terms regarding "Microservice architectures"

* Starts at 1:47:22 in the [video](https://www.youtube.com/watch?v=hmkF77F9TLw).

* Synchronous inter-service communication.
  * The client sends the request..and waits for the response.
  * The client will be blocked whitle waiting: => A "blocking request".
  * Example: THe "API Gateway" communicates with the "auth" service SYNCHRONOUSLY.
    * => The 2 services are "TIGHTLY COUPLED".

* Asynchronous inter-service communication.
  * The client does NOT need to await the response => A non-blocking request.
  * Achieved e.g. by using a QUEUE.
  * => DECOUPLING: "LOOSELY COUPLED" services.
  * => "SEND & FORGET" 
    * (sends a message, and forgets about it => No need to wait for a response).

* Strong consistency 
  * Data will be immediately available.

* Eventual consistency
  * Data vil evntually be available.