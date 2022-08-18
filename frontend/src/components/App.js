import React, { Component } from 'react';
import { render } from "react-dom";
import Table1 from './Table'


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("api/order")
      .then(response => {
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }

  render() {
   let data = this.state.data.map(function(item) {
      return <tr key={item.number}>
         <td>{item.number}</td>
         <td>{item.order_number}</td>
         <td>{item.price_dollars}</td>
         <td>{item.price_rubles}</td>
         <td>{item.delivery_time}</td>
      </tr>;
   });
   const sum = this.state.data.reduce((sum, n) => sum + +n.price_dollars, 0);
    return (
      <div className="App">
        <p className="Table-header">Каналсервис</p>
        <p className="Table-header">TOTAL</p><h1>{sum}$</h1>
        <Table1 data={data}/>
      </div>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);