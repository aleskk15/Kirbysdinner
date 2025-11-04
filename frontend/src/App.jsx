import { useState, useEffect, useRef } from 'react'

function App() {
  let [cliente, setCliente] = useState([]);
  let [mesero, setMesero] = useState([]);
  let [cocinero, setCocinero] = useState([]);
  let [comida, setComida] = useState([]);
  let [silla, setSilla] = useState([]);
  let simSpeed = 1;
  const running = useRef(null);

    let setup = () => {
    console.log("Hola");

    fetch("http://localhost:8000/run", {
    }).then(resp => resp.json())
    .then(data => {
      console.log(data);
      setCliente(data["cliente"] || []);
      setMesero(data["mesero"] || []);
      setCocinero(data["cocinero"] || []);
      setComida(data["comida"] || []);
      setSilla(data["silla"] || []);
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
        setComida(data["comida"] || []);
        setSilla(data["silla"] || []);
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


      {cliente.map(cliente => (<image key={cliente.id} x={255 + 25 * (cliente.pos[1] - 1)} y={9 + 25 * (cliente.pos[0] - 1)} href="pinguino.png" />))}
      {cliente.map(cliente => console.log("cliente", cliente.status, cliente.pos[0], cliente.pos[1]))}

      {mesero.map(mesero => (<image key={mesero.id} x={255 + 25 * (mesero.pos[1] - 1)} y={9 + 25 * (mesero.pos[0] - 1)} href="identificacion-facial.png" />))}    
      {mesero.map(mesero => console.log("mesero", mesero.status, mesero.pos[0], mesero.pos[1]))}

      {comida.filter(itm => itm.status === "lista" || itm.status === "entregada").map(comida => (<image key={comida.id} x={255 + 25 * (comida.posicion[1] -1)} y={9 + 25 * (comida.posicion[0] - 1)} href = {comida.nombre == "bebida" ? "soda.png" : "dieta.png"} />))}
      {comida.map(comida => console.log("comida", comida.status, comida.posicion[0], comida.posicion[1]))}
      

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