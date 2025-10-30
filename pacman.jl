using Agents, Agents.Pathfinding
using Random
@enum Statuscliente llegando sentarse pidiendo comiendo acabando
@enum Statuscocinero recibeOrden cocinaOrden entregaOrden
@enum Statusmesero tomaOrden mandaOrden agarraOrden ordenEntregada
@enum Tiposdecomida bebida plato

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

@agent struct Cliente(GridAgent{2})
    type::String = "Cliente"
    status::Statuscliente = llegando
end

#El dos me dice las dimensiones del grid
@agent struct Mesero(GridAgent{2})
    type::String = "Mesero"
    cliente_id::Int = 0 
    cocinero_id::Int = 0
    status::Statusmesero = tomaOrden
end

@agent struct Cocinero(GridAgent{2})
    type::String = "Cocinero"
    cliente_id::Int = 0 
    Mesero_id::Int = 0   
    status::Statuscocinero = recibeOrden
end

struct Comida
    cliente_id::Int 
    nombre::Tiposdecomida 
end

#por cada tic la función se llama, _agent es como el self de python
# se va a mover con la ruta del pathfinder, por eso se pasa con el diccionario para poder acceder
# Este es el agent_step! correcto
function agent_step!(agent::Cliente, model)
    #if agent.Statuscliente == llegando 
    #   move_along_route!(agent, model, model.pathfinder)
#end
        
        
end


function agent_step!(agent::Cocinero, model)
    x= "Orden recibida en cocina"
    y= "Orden cocinandose en cocina"
    w = "Orden terminada"
    if agent.Statusmesero == mandaOrden
        agent.Statuscocinero == recibeOrden
        print(x)
    elseif agent.Statuscocinero ==recibeOrden
        agent.Statuscocinero == cocinaOrden
        print(y)
    elseif agent.Statuscocinero == cocinaOrden
        agent.Statuscocinero == entregaOrden
        print(w)
    elseif agent.Statuscocinero == entregaOrden
        agent.Statusmesero == agarraOrden
    end
    
end


function agent_step!(agent::Mesero, model)
    inicio_pos = (2, 10) 
    cocina_pos = (11, 6)
    move_along_route!(agent, model, model.pathfinder)
     if agent.pos == inicio_pos
        plan_route!(agent, cocina_pos, pathfinder)
        move_along_route!(agent, model, model.pathfinder)
    elseif agent.pos == cocina_pos
        plan_route!(agent, inicio_pos, pathfinder)
        move_along_route!(agent, model, model.pathfinder)
    end
end


#Se hacen agentes y ambientes
# Usamos el algoritmo estrella de los agentes
 
function initialize_model()
    space = GridSpace((14,17); periodic=false, metric=:manhattan)
    pathfinder = AStar(space; walkmap=lab, diagonal_movement= false)
    properties = Dict(:pathfinder => pathfinder)
    model = StandardABM(Union{Cliente,Mesero,Cocinero}, space; agent_step!, properties)
    posiciones = [(3,3),(6,3),(12,7)]
    pF= shuffle(posiciones)[1:1]
    final = pF[1]
    add_agent!((2,2),Mesero, model)

    print(final)

    plan_route!(model[1], final, pathfinder)


    return model, pathfinder
end


model, pathfinder = initialize_model()