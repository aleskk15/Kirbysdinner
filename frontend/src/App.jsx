import { useState, useEffect, useRef } from 'react'

function App() {
  let [cliente, setCliente] = useState([]);
  let [mesero, setMesero] = useState([]);
  let [cocinero, setCocinero] = useState([]);
  let simSpeed = 1;
  const running = useRef(null);

    let setup = () => {
    console.log("Hola");

    fetch("http://localhost:8000/setup", {
    }).then(resp => resp.json())
    .then(data => {
      console.log(data);
      setCliente(data["cliente"] || []);
      setMesero(data["mesero"] || []);
      setCocinero(data["cocinero"] || []);
    })
    .catch(error => console.error("Error during setup fetch:", error));
  }

  useEffect(() => {
        setup();
    }, []);

  const handleStart = () => {
    running.current = setInterval(() => {
      fetch("http://localhost:8000/run")
      .then(res => res.json())
      .then(data => {
        setCliente(data["cliente"] || []);
        setMesero(data["mesero"] || []);
        setCocinero(data["cocinero"] || []);
      })
      .catch(error => console.error("Error fetching data:", error));
    }, 1000 / simSpeed);
  };

  const handleStop = () => {
      if (running.current) {
          clearInterval(running.current);
          running.current = null;
      }
  };



  let matrix = [
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
   [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
   [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
   [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
   [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
   [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],  
   [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],
   [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
   [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
   [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
   [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]



  return (

    <div>
    <div>
      <svg width="800" height="500" xmlns="http://www.w3.org/2000/svg">
      {
        matrix.map((row, rowidx) =>
        row.map((value, colidx) =>
          <rect x={250 + 25 * colidx} y={5 + 25 * rowidx} width={25} height={25} fill={value == 1 ? "lightgray" : "gray"} />
      ))

      }


      {cliente.map(cliente => (<image key={cliente.id} x={255 + 25 * cliente.pos[0]} y={9 + 25 * cliente.pos[1]} href="pinguino.png" />))}
      {cliente.map(cliente => console.log(cliente.status))}

      {mesero.map(mesero => (<image key={mesero.id} x={255 + 25 * mesero.pos[0]} y={9 + 25 * mesero.pos[1]} href="identificacion-facial.png" />))}    
      {mesero.map(mesero => console.log(mesero.status))}
      </svg>
    </div>


    <div>
    <button onClick={handleStart}>Start</button>
    </div>
    <div>
    <button onClick={handleStop}>Stop</button>
    </div>




    </div>
  );
};

export default App;