using Agents, Agents.Pathfinding
#el arroba es una decoracion que viene con el paquete agents, le dice al compilador que hay codigo repetitivo e inserta el codigo repetittivo a la estructura
matrix = [
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
  0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 0;
  0 1 0 1 0 0 0 1 1 1 0 1 0 1 0 1 0;
  0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 0;
  0 1 0 0 0 1 1 1 1 1 1 1 0 0 0 1 0;
  0 1 0 1 0 1 0 0 0 0 0 1 1 1 0 1 0;
  0 1 1 1 0 1 0 1 1 1 0 1 0 1 0 1 0;
  0 1 0 1 0 1 0 1 1 1 0 1 0 1 0 1 0;
  0 1 0 1 1 1 0 0 1 0 0 1 0 1 1 1 0;
  0 1 0 0 0 1 1 1 1 1 1 1 0 0 0 1 0;
  0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 0;
  0 1 0 1 0 1 0 1 1 1 0 0 0 1 0 1 0;
  0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 0;
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
];



@agent struct Ghost(GridAgent{2}) 
    type::String = "Ghost"
end

function initialize_model() 
    maze = BitArray(matrix)
    space = GridSpace(size(maze); periodic = false, metric = :manhattan) #distancia manhattan darle la vuelta a la manzana
    pathfinder = AStar(space; walkmap = maze, diagonal_movement=false)
    model = StandardABM(Ghost, space; agent_step!) #los primeros son los atributos posicionales, : despues del ; son los parametros metricos
    add_agent!(Ghost, pos=(2, 2), model) #le estoy diciendo que aparece un agente de tipo ghost y aparece en la posicion 3, 3
    
    plan_route!(model[1], (13, 16), pathfinder)
    return model, pathfinder
end

#LLamas a la funcion con sus agentes, es como un self en python
agent_step!(agent, model) = move_along_route!(agent, model,pathfinder)


model, pathfinder = initialize_model() #variables que son globales
