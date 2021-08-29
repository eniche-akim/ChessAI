var board,
  game = new Chess(),
  statusEl = $('#status'),
  fenEl = $('#fen'),
  pgnEl = $('#pgn');



// do not pick up pieces if the game is over
// only pick up pieces for the side to move
var onDragStart = function(source, piece, position, orientation) {
  if (game.game_over() === true ||
      (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
  }
};

var onDrop = function(source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  });

  // illegal move
  if (move === null) return 'snapback';

  updateStatus();
  getResponseMove();
};

// update the board position after the piece snap
// for castling, en passant, pawn promotion
var onSnapEnd = function() {
    board.position(game.fen());
};

var updateStatus = function() {
  var status = '';

  var moveColor = 'White';
  if (game.turn() === 'b') {
    moveColor = 'Black';
  }

  // checkmate?
  if (game.in_checkmate() === true) {
    status = 'Game over, ' + moveColor + ' is in checkmate.';
  }

  // draw?
  else if (game.in_draw() === true) {
    status = 'Game over, drawn position';
  }

  // game still on
  else {
    status = moveColor + ' to move';

    // check?
    if (game.in_check() === true) {
      status += ', ' + moveColor + ' is in check';
    }
  }

  setStatus(status);
  getLastCapture();
  createTable();
  updateScroll();
  
  statusEl.html(status);
  fenEl.html(game.fen());
  pgnEl.html(game.pgn());
};

var cfg = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
};

var randomResponse = function() {
    fen = game.fen()
    $.get($SCRIPT_ROOT + "/move/" + fen, function(data) {
        game.move(data, {sloppy: true});
        // board.position(game.fen());
        
        updateStatus();
    })
}

var getResponseMove = function() {
    var e = document.getElementById("sel1");
    var depth = e.options[e.selectedIndex].value;
    fen = game.fen()
    $.get($SCRIPT_ROOT + "/move/" + fen, function(data) {
    	const words = data.split(' ');
        game.move(words[0], {sloppy: true});

		update_bar(words[2]);
        updateStatus();
        // This is terrible and I should feel bad. Find some way to fix this properly.
        // The animations would stutter when moves were returned too quick, so I added a 100ms delay before the animation
        setTimeout(function(){ board.position(game.fen()); }, 100);
    })
}


// did this based on a stackoverflow answer
// http://stackoverflow.com/questions/29493624/cant-display-board-whereas-the-id-is-same-when-i-use-chessboard-js
setTimeout(function() {
    board = ChessBoard('board', cfg);
    // updateStatus();
}, 0);


var setPGN = function() {
  var table = document.getElementById("pgn");
  var pgn = game.pgn().split(" ");
  var move = pgn[pgn.length - 1];
}

var createTable = function() {

    var pgn = game.pgn().split(" ");
    var data = [];

    for (i = 0; i < pgn.length; i += 3) {
        var index = i / 3;
        data[index] = {};
        for (j = 0; j < 3; j++) {
            var label = "";
            if (j === 0) {
                label = "moveNumber";
            } else if (j === 1) {
                label = "whiteMove";
            } else if (j === 2) {
                label = "blackMove";
            }
            if (pgn.length > i + j) {
                data[index][label] = pgn[i + j];
            } else {
                data[index][label] = "";
            }
        }
    }

    $('#pgn tr').not(':first').remove();
    var html = '';
    for (var i = 0; i < data.length; i++) {
        html += '<tr><td>' + data[i].moveNumber + '</td><td>'
        + data[i].whiteMove + '</td><td>'
        + data[i].blackMove + '</td></tr>';
    }

    $('#pgn tr').first().after(html);
}

var updateScroll = function() {
    $('#moveTable').scrollTop($('#moveTable')[0].scrollHeight);
}

var setStatus = function(status) {
  document.getElementById("status").innerHTML = status;
}

var takeBack = function() {
    game.undo();
    if (game.turn() != "w") {
        game.undo();
    }
    board.position(game.fen());
    updateStatus();
}

var newGame = function() {
    game.reset();
    board.start();
    updateStatus();
    
}

var getCapturedPieces = function() {
    var history = game.history({ verbose: true });
    for (var i = 0; i < history.length; i++) {
        if ("captured" in history[i]) {
            console.log(history[i]["captured"]);
        }
    }
}

var getLastCapture = function() {
    var history = game.history({ verbose: true });
    var index = history.length - 1;

    if (history[index] != undefined && "captured" in history[index]) {
        console.log(history[index]["captured"]);
    }
}

class Timer {

    constructor(player, minutes = 0) {
      this.player = player;
      this.minutes = minutes;
      this.secondes = 0;
      this.hz = 0;
      }
      
	display_secondes(displayID){
		  display_black = document.querySelector(displayID);
      }
      
    padZero(time){
      if (time < 10){return '0' + time;}
      return time;
      }
      
    decrement_time(){
      if (this.hz === 0 && this.secondes === 0){
      	this.hz = 10;
      	this.secondes = 60;
      	this.minutes = this.minutes - 1;
      	}
      else if (this.hz === 0){
      	this.hz = 10;
        this.secondes = this.secondes - 1;
        }
      else{
      	this.hz = this.hz - 1;}

      	}
      
  	display_time(id){
    	document.getElementById(id).textContent = this.padZero(this.minutes) + ':' + this.padZero(this.secondes) +':' + this.padZero(this.hz);
  		}


}
var StartGame = function (){
  
  let players = create_players()
  let p1time = players.p1time
  let p2time = players.p2time 
     
  let timerId = setInterval(function(){
    
    if (game.turn() == p1time.player){
		
       p1time.decrement_time(); 
       p1time.display_time("timeW");

    
        if (p1time.secondes === 0 && p1time.minutes === 0 && p1time.hz === 0){
          game.game_over() = true;
          clearInterval(timerId);
          }
        }
        
    else{
  
         p2time.decrement_time();	
        p1time.display_time("timeB");
        		
            if (p2time.secondes === 0 && p2time.minutes === 0 && p2time.hz === 0){
              game.game_over = true;
              clearInterval(timerId);
              }
            }
          
        }, 100);

}
// Create an instance of the timer for each player.
create_players = function (){
	var e = document.getElementById("sel1");
	var minutes = e.options[e.selectedIndex].value;
	let p1time = new Timer('w', minutes);
	let p2time = new Timer('b', minutes);
	return {p1time, p2time}
}

var update_bar = function(height) {

	var elem = document.getElementById("bar");
	elem.style.height = height + "%";
}


