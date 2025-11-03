using Agents, Agents.Pathfinding
using Random
@enum Statuscliente llegando sentarse pidiendo esperando comiendo acabando
@enum Statuscocinero recibeOrden cocinaOrden 
@enum Statusmesero tomaOrden agarraOrden mandaOrden ordenEntregada
@enum Tiposdecomida bebida plato
@enum Statuscomida orden preparando lista entregada

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

@show lab[13,10]
@show lab[10,13]
@show lab[11,13]
@show lab[11,11]
@show lab[5, 10]

@agent struct Cliente(GridAgent{2})
    type::String = "Cliente"
    status::Statuscliente = llegando
    cont::Int = 0
end

#El dos me dice las dimensiones del grid
@agent struct Mesero(GridAgent{2})
    type::String = "Mesero"
    cliente_id::Int = 0 
    cocinero_id::Int = 0                
    status::Statusmesero = tomaOrden
    cont::Int = 0
end

@agent struct Cocinero(GridAgent{2})
    type::String = "Cocinero"
    cliente_id::Int = 0 
    Mesero_id::Int = 0   
    status::Statuscocinero = recibeOrden
    cont::Int = 0
end

 mutable struct Comida
    cliente_id::Int 
    nombre::Tiposdecomida
    status::Statuscomida
    posicion::Tuple{Int,Int}
end

mutable struct Silla
    ocupado::Bool
    posicion::Tuple{Int,Int}
    cliente_id::Int
end


function agent_step!(agent::Cliente, model)
    if agent.status == llegando
        sillas = abmproperties(model)[:sillas]
        pathfinder = abmproperties(model)[:pathfinder]

        for silla in sillas
            if !silla.ocupado
                # Aqui se mueve a la silla
                plan_route!(agent, silla.posicion, pathfinder)
                move_along_route!(agent, model, pathfinder)
                #Vemos si ya llego 
                if agent.pos == silla.posicion
                    silla.ocupado = true
                    silla.cliente_id = agent.id
                    agent.status = sentarse
                    print("llegue")
                end
                break
    
            end
        end

    elseif agent.status == sentarse
        #Aqui se debe poner una instruccion para la coneccion en el opengl
        agent.cont += 1
        if agent.cont >= 5
            agent.status = pidiendo
            agent.cont = 0
        end

    elseif agent.status == pidiendo
        print("pidiendo")
        comidas = abmproperties(model)[:comidas]
        ordencl = Comida(agent.id, plato, orden, (1,1))
        push!(comidas, ordencl)
        agent.status = esperando
         
    elseif agent.status == esperando
        print("esperando")
        if haskey(abmproperties(model), :comidas)
            comidas = abmproperties(model)[:comidas]
            for comida in comidas
                if comida.cliente_id == agent.id && comida.status == entregada
                    agent.status = comiendo
                    comida.posicion = agent.pos
                    #deleteat!(comidas, findfirst(x -> x.cliente_id == agent.id, comidas))
                    break
                end
            end
        end
        

    elseif agent.status == comiendo
        agent.cont += 1
        if agent.cont  >= 15
            agent.status = acabando
            comidas = abmproperties(model)[:comidas]
            deleteat!(comidas, findfirst(x -> x.cliente_id == agent.id, comidas))

            agent.cont = 0
        end

    elseif agent.status == acabando
        pathfinder = abmproperties(model)[:pathfinder]
        sillas = abmproperties(model)[:sillas]
        plan_route!(agent, (10,13), pathfinder)
        move_along_route!(agent, model, pathfinder)
        if agent.pos == (10,13)
            silla = findfirst(s -> s.cliente_id == agent.id, sillas)
            if silla !== nothing
                sillas[silla].ocupado = false
                sillas[silla].cliente_id = 0
            end
            kill_agent!(agent, model)
        end
    end

end


function agent_step!(agent::Cocinero, model)
    if haskey(abmproperties(model), :comidas)
            comidas = abmproperties(model)[:comidas]
            for comida in comidas
                if comida.status == orden && agent.status == recibeOrden
                    comida.status = preparando
                    agent.status = cocinaOrden
                    break
                elseif comida.status == preparando && agent.status == cocinaOrden
                    agent.cont += 1
                    if agent.cont >= 15
                        comida.posicion = (11, 11)
                        comida.status = lista
                        agent.status = recibeOrden 
                        agent.cont = 0
                    end
            
                end
            end
        end
end

function agent_step!(agent::Mesero, model)
    if agent.status == tomaOrden
        print("tomando orden")
        if haskey(abmproperties(model), :comidas)
            comidas = abmproperties(model)[:comidas]
            pathfinder = abmproperties(model)[:pathfinder]

            for comida in comidas
                if comida.status == lista 
                    agent.cliente_id = comida.cliente_id
                    print(comida.posicion)
                    plan_route!(agent, (comida.posicion), pathfinder)
                    move_along_route!(agent, model, pathfinder)
                    if agent.pos == comida.posicion 
                        agent.status = agarraOrden
                        println("Mesero agarró la orden para el cliente $(agent.cliente_id)")
                    end
                    break
                end
            end
        end 
    elseif agent.status == agarraOrden
        agent.cont += 1
        if agent.cont >= 5
            agent.status = mandaOrden
            agent.cont = 0
        end
    elseif agent.status == mandaOrden
        pathfinder = abmproperties(model)[:pathfinder]
        comidas = abmproperties(model)[:comidas]

        comida_idx = findfirst(c -> c.cliente_id == agent.cliente_id, comidas)
        if comida_idx !== nothing
            comida = comidas[comida_idx]
            #comida.posicion = agent.pos


            for otheragent in allagents(model)
                if otheragent isa Cliente && agent.cliente_id == otheragent.id

                    plan_route!(agent, (otheragent.pos[1], otheragent.pos[2]), pathfinder)
                    move_along_route!(agent, model, pathfinder)
                    comida.posicion = agent.pos


                    if agent.pos == (otheragent.pos[1], otheragent.pos[2])
                        agent.status = ordenEntregada
                        comidas[comida_idx].status = entregada
                        println("Mesero entregó la orden al cliente $(agent.cliente_id)")
                    end
                end
            end
        end

    elseif agent.status == ordenEntregada
        agent.cont += 1
        if agent.cont >= 5
            agent.status = tomaOrden
            agent.cont = 0
        end
    
    end

end

#Se hacen agentes y ambientes
# Usamos el algoritmo estrella de los agentes
 
function initialize_model()
    space = GridSpace((14,17); periodic=false, metric=:manhattan)
    pathfinder = AStar(space; walkmap=lab, diagonal_movement= false)
    posiciones = [(3,3),(6,3),(12,7)]
    pF= shuffle(posiciones)[1:1]
    final = pF[1]
    sillas = [
        Silla(false, (3, 3), 0),
        Silla(false, (6, 3), 0),
        Silla(false, (12, 7), 0)
    ]
    properties = Dict(:pathfinder => pathfinder, :comidas => Comida[], :sillas => sillas)
    model = StandardABM(Union{Cliente,Mesero,Cocinero}, space; agent_step!, properties)


    add_agent!((1,1), Cocinero, model)
    add_agent!((5,10), Mesero, model)
    add_agent!((2,16), Cliente, model)
    
    print(final)


    return model, pathfinder
end


model, pathfinder = initialize_model()