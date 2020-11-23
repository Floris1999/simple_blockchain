import React, { useState, useEffect } from "react";
import { blockchainService } from "./_services";

import {
  Card,
  Button,
  Container,
  Row,
  Col,
  Form,
  CardDeck,
  Jumbotron,
  Accordion,
  Table,
  Alert
} from "react-bootstrap";

function App() {
  const [input, setInput] = useState("");

  const [sender, setSender] = useState("");
  const [recipient, setRecipient] = useState("");
  const [amount, setAmount] = useState("");

  const [transactions, setTransactions] = useState(null);
  const [wallets, setWallets] = useState(null);
  const [show, setShow] = useState(true);

  useEffect(() => {
    // blockchainService.getAll();
    blockchainService.getAll().then((x) => {
      setWallets(x.wallet);
    });

    blockchainService.getTransactions().then((x) => {
      console.log(x.chain);
      setTransactions(x.chain);
    });
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    input.address = makeAddress(32);
    let response = await blockchainService.createWallet(input);
    // console.log(response);
    setWallets(response.wallet);

    // console.log(input);
  }

  async function handleTransaction(event) {
    event.preventDefault();
    console.log(sender);
    let body = {
      sender: sender,
      recipient: recipient,
      amount: parseInt(amount),
    };
    // console.log(body);

    // window.location.reload();
    // console.log(input);
    let response = await blockchainService.createTransaction(body);
    setTransactions(response.chain);
    setWallets(response.wallet)
    // setTransactions(response.wallet);
  }

  function makeAddress(length) {
    var result = "";
    var characters = "abcdefghijklmnopqrstuvwxyz0123456789";
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
  }

  function mine() {
    blockchainService.mine();
    window.location.reload(); 
  }

  return (
    <Container>
      <Row>
        <Col>
          <div className="App">
            <header className="App-header">
              <Jumbotron>
                <h1>Hello, world!</h1>
                <p>
                  This is a very simple webapp to interact with a self made
                  blockchain. This app is not in any way usable for production.
                </p>

                <p>
                  <Button variant="primary" onClick={mine}>
                    Start mining
                  </Button>
                </p>

                <Accordion>
                  <Card>
                    <Card.Header>
                      <Accordion.Toggle as={Button} variant="link" eventKey="0">
                        Current transaction in the chain
                      </Accordion.Toggle>
                    </Card.Header>
                    <Accordion.Collapse eventKey="0">
                      <Card.Body>
                        <Table striped bordered hover variant="dark">
                          <thead>
                            <tr>
                              <th>#</th>
                              <th>Sender address</th>
                              <th>Recipient addres</th>
                              <th>amount</th>
                            </tr>
                          </thead>
                          <tbody>
                            {transactions &&
                              transactions.map((transaction, index) => (
                                <tr key={index}>
                                  <td>{index}</td>
                                  <td>{transaction.sender}</td>
                                  <td>{transaction.recipient}</td>
                                  <td>{transaction.amount}</td>
                                </tr>
                              ))}
                          </tbody>
                        </Table>
                      </Card.Body>
                    </Accordion.Collapse>
                  </Card>
                </Accordion>
              </Jumbotron>
              <CardDeck>
                <Card style={{ width: "18rem" }}>
                  <Card.Body>
                    <Card.Title>Add user</Card.Title>
                    <Card.Text>
                      Here you can create a new wallet for an user
                    </Card.Text>
                    <Form onSubmit={handleSubmit}>
                      <Form.Group controlId="formWallet">
                        <Form.Label>Name</Form.Label>
                        <Form.Control
                          type="Name"
                          placeholder="Enter name"
                          // value={this.state.val}
                          onChange={(e) => setInput({ name: e.target.value })}
                        />
                      </Form.Group>
                      <Button variant="primary" type="submit">
                        Submit
                      </Button>
                    </Form>
                  </Card.Body>
                </Card>

                <Card style={{ width: "18rem" }}>
                  <Card.Body>
                    <Card.Title>New transaction</Card.Title>
                    <Card.Text>Here you can send money to a wallet</Card.Text>
                    <Form onSubmit={handleTransaction}>
                      <Form.Group controlId="formWallet">
                        <Form.Label>Sender adress</Form.Label>
                        <Form.Control
                          required
                          type="Sender address"
                          placeholder="Enter name"
                          // value={this.state.val}
                          onChange={(e) => setSender(e.target.value)}
                        />
                        <Form.Control
                          required
                          type="Name"
                          placeholder="Recipient address"
                          // value={this.state.val}
                          onChange={(e) => setRecipient(e.target.value)}
                        />

                        <Form.Control
                          required
                          type="Number"
                          placeholder="Amount"
                          // value={this.state.val}
                          onChange={(e) => setAmount(e.target.value)}
                        />
                      </Form.Group>

                      <Button variant="primary" type="submit">
                        Submit
                      </Button>
                    </Form>
                  </Card.Body>
                </Card>
              </CardDeck>
            </header>
          </div>
        </Col>
      </Row>
      <br />
      <br />
      <Col className="container-fluid mt-4">
        <CardDeck>
          {wallets &&
            wallets.map((wallet) => (
              <Card key={wallet.address} style={{ width: "18rem" }}>
                <Card.Body>
                  <Card.Title>{wallet.name}</Card.Title>
                  <Card.Text>
                    Address: {wallet.address}
                    <br />
                    Balance: {wallet.balance}
                  </Card.Text>
                </Card.Body>
                <Card.Footer>
                  <small className="text-muted"></small>
                </Card.Footer>
              </Card>
            ))}
        </CardDeck>
      </Col>
    </Container>
  );
}

export default App;
