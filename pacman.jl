using Agents

#el arroba es una decoracion que viene con el paquete agents, le dice al compilador que hay codigo repetitivo e inserta el codigo repetittivo a la estructura
@agent struct Ghost(GridAgent{2}) 
    type::String = "Ghost"
end
const matrix = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
  [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
  [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
  [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
  [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
  [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
  [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
  [0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0],
  [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
  [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
  [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0],
  [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

#LLamas a la funcion con sus agentes, es como un self en python
function agent_step!(agent, model)
    vecinos = [(1,0), (-1,0), (0,1), (0,-1)]
    validos = []
    for (dx, dy) in vecinos
        nPos = (agent.pos[1] + dx, agent.pos[2] + dy) 
        if  matrix[nPos[2]][nPos[1]] == 1          
            push!(validos, nPos)
        end
    end
    if !isempty(validos)
        move_agent!(agent, rand(validos), model)
    end
end

function initialize_model() 
    space = GridSpace((17,14); periodic = false, metric = :manhattan) #distancia manhattan darle la vuelta a la manzana
    model = StandardABM(Ghost, space; agent_step!) #los primeros son los atributos posicionales, : despues del ; son los parametros metricos
    return model
end

model = initialize_model() #variables que son globales
a = add_agent!(Ghost, pos=(2, 2), model) #le estoy diciendo que aparece un agente de tipo ghost y aparece en la posicion 3, 3
