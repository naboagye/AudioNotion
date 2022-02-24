// [START container_hello_app]
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/kubemq-io/kubemq-go"
)

type NotionLink struct {
	Name  string `json:"name"`
	ID    int    `json:"id"`
	URL   string `json:"url"`
	Email string `json:"email"`
}

// func main() {
// 	params := url.Values{}
// 	params.Add("title", "foo")
// 	params.Add("body", "bar")
// 	params.Add("userId", "1")
// 	// register hello function to handle all requests
// 	mux := http.NewServeMux()
// 	mux.HandleFunc("/my-handling-form-page", sendMsg).Methods("POST")

// 	// use PORT environment variable, or default to 8080
// 	port := os.Getenv("PORT")
// 	if port == "" {
// 		port = "8080"
// 	}

// 	// start the web server on port and accept requests
// 	log.Printf("Server listening on port %s", port)
// 	log.Fatal(http.ListenAndServe(":"+port, mux))
// }

// hello responds to the request with a plain-text "Hello, world" message.
// func hello(w http.ResponseWriter, r *http.Request) {
// 	log.Printf("Serving request: %s", r.URL.Path)
// 	host, _ := os.Hostname()
// 	fmt.Fprintf(w, "Hello, world!\n")
// 	fmt.Fprintf(w, "Version: 1.0.0\n")
// 	fmt.Fprintf(w, "Hostname: %s\n", host)
// }

func sendMsg(w http.ResponseWriter, r *http.Request) {
	reqBody, _ := ioutil.ReadAll(r.Body)
	var post NotionLink
	json.Unmarshal(reqBody, &post)

	json.NewEncoder(w).Encode(post)
	newData, err := json.Marshal(post)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(string(newData))
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	client, err := kubemq.NewClient(ctx,
		kubemq.WithAddress("localhost", 50000),
		kubemq.WithClientId("test-command-client-id"),
		kubemq.WithTransportType(kubemq.TransportTypeGRPC))
	if err != nil {
		log.Fatal(err)
	}
	defer client.Close()
	channel := "my-queue"

	sendResult, err := client.NewQueueMessage().
		SetChannel(channel).
		SetBody([]byte(newData)).
		Send(ctx)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Fprintf(w, "Send to Queue Result: MessageID:%s,Sent At: %s\n", sendResult.MessageID, time.Unix(0, sendResult.SentAt).String())
	log.Printf("Send to Queue Result: MessageID:%s,Sent At: %s\n", sendResult.MessageID, time.Unix(0, sendResult.SentAt).String())
}

func handleReqs() {
	r := mux.NewRouter().StrictSlash(true)
	r.HandleFunc("/post", sendMsg).Methods("POST")

	log.Fatal(http.ListenAndServe(":8000", r))
}

func main() {
	handleReqs()
}

// [END container_hello_app]
