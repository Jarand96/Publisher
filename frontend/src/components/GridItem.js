import React, { Component } from "react";
import {store} from "react";
import { connect } from 'react-redux';


class GridItem extends Component {
  constructor(props) {
   super(props);
   const {dispatch} = props;
   this.gridItem = React.createRef();
   this.state = {
     dragging: false,
     startX:'',
     startY:''
   }

 // This binding is necessary to make `this` work in the callback
 this._onMouseUp = this._onMouseUp.bind(this)
 }

  componentDidUpdate() {
    if (this.state.dragging) {
      //document.addEventListener('mousemove', this.onMouseMove)
      document.addEventListener('mouseup', this._onMouseUp)
    } else if (!this.state.dragging) {
      //document.removeEventListener('mousemove', this.onMouseMove)
      document.removeEventListener('mouseup', this._onMouseUp)
    }
  }

  _onMouseDown(e){
    if (e.button !== 0) return
    this.props.dispatch({type: "_SET_FOCUS_OBJECT", payload: {
      'index': this.props.index,
      'object': this.props.object
    }});
    this.setState({
      dragging:true,
      startX: e.clientX,
      startY: e.clientY
    })
    e.stopPropagation()
    e.preventDefault()
  }

  _onMouseUp(e){
    /*The user if finished dragging the object. and lets go.
    *Check how many pixels the mouse moved in X direction. Over half the size of 1 cell?
    If yes, check freeSpace() with object in focus properties + the new x value
    *if yes, run the moveX function and pass in the amount of cells
    */
    console.log(this.state.startX)
    console.log(e.clientX);
    console.log("The difference in X-position is: " + (e.clientX - this.state.startX))
    console.log("The width of one cell is: " + this.props.advancedPost.gridCellWidth)
    this.setState({
      dragging: false
    })
    let deltaX = e.clientX - this.state.startX
    let gridCellWidth = this.props.advancedPost.gridCellWidth
    let steps = Math.ceil(deltaX/gridCellWidth)
    console.log("The number of steps to move: " + steps)
    this.props.dispatch({type: "_MOVE_DIV_X", payload: steps});
    e.stopPropagation()
    e.preventDefault()

  }
  _onMouseMove(e) {
      if (!this.state.dragging) return
      //Reconsider the code below to see if it can be used.
      //The on move is used to show the user if the operation is possible or not.
      //e.g the user drags a div, set dragging to true, and this function updates the grid
      //with colors giving a visual representation whether the space is free or not.
     const position = this.gridItem.current.getBoundingClientRect();
     this.setState({ x: e.nativeEvent.offsetX, y: e.nativeEvent.offsetY });
  }

  render(){
    const object = this.props.object
    const index = this.props.index
    let div_style = {
      gridColumnStart: object.column_start,
      gridColumnEnd: object.column_start + object.width,
      gridRowStart: object.row_start,
      gridRowEnd: object.row_start + object.height,
      backgroundColor : object.backgroundColor
    }
    const { startX, startY } = this.state;
  	return (
      <div
        ref={this.gridItem}
        onMouseMove={this._onMouseMove.bind(this)}
        onMouseDown={this._onMouseDown.bind(this)}
        onMouseUp={this._onMouseUp.bind(this)}
        onClick={() => {
        }
      }
      style={div_style}>
        {object.text} X:{startX} Y:{startY}
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
      forms: state.form,
      auth: state.auth,
      posts: state.posts,
      user: state.user,
      advancedPost: state.advancedPost
    };
}

export default connect(
  mapStateToProps,
)(GridItem);