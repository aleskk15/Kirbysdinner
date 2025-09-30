using Agents

#el arroba es una decoracion que viene con el paquete agents, le dice al compilador que hay codigo repetitivo e inserta el codigo repetittivo a la estructura
@agent struct Ghost(GridAgent{2}) 
    type::String = "Ghost"
end

#LLamas a la funcion con sus agentes, es como un self en python
function agent_step!(agent, model)
    randomwalk!(agent, model)
end

function initialize_model() 
    space = GridSpace((5,5); periodic = false, metric = :manhattan) #distancia manhattan darle la vuelta a la manzana
    model = StandardABM(Ghost, space; agent_step!) #los primeros son los atributos posicionales, : despues del ; son los parametros metricos
    return model
end

model = initialize_model() #variables que son globales
a = add_agent!(Ghost, pos=(3, 3), model) #le estoy diciendo que aparece un agente de tipo ghost y aparece en la posicion 3, 3
