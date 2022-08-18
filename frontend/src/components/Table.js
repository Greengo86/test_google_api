import React, { Component } from 'react';


class Table1 extends Component {
  render() {
    return <table>
          <thead>
             <tr>
                <td>№</td>
                <td>Заказ №</td>
                <td>Стоимость, $</td>
                <td>Стоимость, рубли</td>
                <td>Срок поставки</td>
             </tr>
          </thead>
          <tbody>
             {this.props.data}
          </tbody>
       </table>;
  }
}

export default Table1;