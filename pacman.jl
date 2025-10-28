using Agents, Agents.Pathfinding

matrix = [
   0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
   0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0;
   0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0;
   0 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 0;
   0 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 0;
   0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0;
   0 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 0;  
   0 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 0;
   0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0;
   0 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 0;
   0 1 1 1 0 0 1 1 1 1 1 1 1 1 1 1 0;
   0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0;
   0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
   0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
]

lab = BitArray(matrix)

#El dos me dice las dimensiones del grid
@agent struct Ghost(GridAgent{2})
    type::String = "Ghost"
end

#por cada tic la función se llama, _agent es como el self de python
# se va a mover con la ruta del pathfinder, por eso se pasa con el diccionario para poder acceder
# Este es el agent_step! correcto
function agent_step!(agent, model)
    x = "llegue"
    move_along_route!(agent, model, model.pathfinder)
        if agent.pos == (5, 11)
            plan_route!(agent, (4, 12), pathfinder)
            move_along_route!(agent, model, model.pathfinder)
        end
        if agent.pos == (4, 12)
            plan_route!(agent, (5, 11), pathfinder)
            move_along_route!(agent, model, model.pathfinder)
        end
        end



#Se hacen agentes y ambientes
# Usamos el algoritmo estrella de los agentes 
function initialize_model()
    space = GridSpace((14,17); periodic=false, metric=:manhattan)
    pathfinder = AStar(space; walkmap=lab, diagonal_movement= false)

    properties = Dict(:pathfinder => pathfinder)
    model = StandardABM(Ghost, space; agent_step!, properties)

    add_agent!((2,2),Ghost, model)

    plan_route!(model[1], (5,11), pathfinder)


    return model, pathfinder
end


model, pathfinder = initialize_model()