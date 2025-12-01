using Agents, Agents.Pathfinding
using Random

@enum Statuscliente llegando sentarse pidiendo esperando comiendo acabando
@enum Statuscocinero recibeOrden buscaIngrediente recogeIngrediente regresaCocina cocinaOrden 
@enum Statusbartender recibeBebida preparaBebida entregaBebida bebidaEntregada
@enum Statusmesero tomaOrden agarraOrden mandaOrden ordenEntregada
@enum Tiposdecomida bebida plato
@enum Platos hamburguesa manzana 
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

@agent struct Cliente(GridAgent{2})
    type::String = "Cliente"
    status::Statuscliente = llegando
    cont::Int = 0
    isMoving::Bool = false
end

@agent struct Mesero(GridAgent{2})
    type::String = "Mesero"
    cliente_id::Int = 0 
    cocinero_id::Int = 0                
    status::Statusmesero = tomaOrden
    cont::Int = 0
    isMoving::Bool = false
end

@agent struct Cocinero(GridAgent{2})
    type::String = "Cocinero"
    cliente_id::Int = 0 
    Mesero_id::Int = 0   
    status::Statuscocinero = recibeOrden
    cont::Int = 0
    isMoving::Bool = false
    posicion_cocina::Tuple{Int,Int} = (12,11)
    tiene_ingrediente::Bool = false
    tipo_comida::Union{Platos, Nothing} = nothing
end

@agent struct Bartender(GridAgent{2})
    type::String = "Bartender"
    cliente_id::Int = 0 
    status::Statusbartender = recibeBebida
    cont::Int = 0
    isMoving::Bool = false
    posicion_barra::Tuple{Int,Int} = (12,10) 
end

mutable struct Comida
    cliente_id::Int 
    nombre::Tiposdecomida
    tipo_plato::Union{Platos, Nothing} 
    status::Statuscomida
    posicion::Tuple{Int,Int}
end

struct Ingredientes
    nombre::Platos
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
                plan_route!(agent, silla.posicion, pathfinder)
                move_along_route!(agent, model, pathfinder)
                agent.isMoving = true
                if agent.pos == silla.posicion
                    agent.isMoving = false
                    silla.ocupado = true
                    silla.cliente_id = agent.id
                    agent.status = sentarse
                    println("Cliente $(agent.id) llegó a la silla")
                end
                break
            end
        end

    elseif agent.status == sentarse
        agent.cont += 1
        if agent.cont >= 5
            agent.status = pidiendo
            agent.cont = 0
        end

    elseif agent.status == pidiendo
        println("Cliente $(agent.id) pidiendo")
        comidas = abmproperties(model)[:comidas]
        pedido = [plato, bebida]
        pedidoFR = shuffle(pedido)
        pedidoFINAL = pedidoFR[1]
        
        tipo_plato = nothing
        if pedidoFINAL == plato
            opciones = [hamburguesa, manzana]
            tipo_plato = rand(opciones)
            println("Cliente $(agent.id) pidió $(tipo_plato)")
        else
            println("Cliente $(agent.id) pidió bebida")
        end
        
        ordencl = Comida(agent.id, pedidoFINAL, tipo_plato, orden, (1,1))
        push!(comidas, ordencl)
        agent.status = esperando
         
    elseif agent.status == esperando
        if haskey(abmproperties(model), :comidas)
            comidas = abmproperties(model)[:comidas]
            for comida in comidas
                if comida.cliente_id == agent.id && comida.status == entregada
                    agent.status = comiendo
                    comida.posicion = agent.pos
                    println("Cliente $(agent.id) comenzó a comer")
                    break
                end
            end
        end

    elseif agent.status == comiendo
        agent.cont += 1
        if agent.cont >= 15
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
        agent.isMoving = true
        if agent.pos == (10,13)
            agent.isMoving = false
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
        pathfinder = abmproperties(model)[:pathfinder]
        ingredientes = abmproperties(model)[:ingredientes]
        
        for comida in comidas
            if comida.nombre == plato && comida.status == orden && agent.status == recibeOrden
                agent.cliente_id = comida.cliente_id
                comida.status = preparando
                agent.status = buscaIngrediente
                agent.tiene_ingrediente = false
                agent.tipo_comida = comida.tipo_plato
                println("Cocinero recibió orden de $(comida.tipo_plato) para cliente $(comida.cliente_id)")
                break
                
            elseif comida.nombre == plato && comida.status == preparando && agent.status == buscaIngrediente
                ingrediente_necesario = findfirst(ing -> ing.nombre == comida.tipo_plato, ingredientes)
                if ingrediente_necesario !== nothing && !agent.tiene_ingrediente
                    ingrediente = ingredientes[ingrediente_necesario]
                    plan_route!(agent, (ingrediente.posicion[1] + 1, ingrediente.posicion[2]), pathfinder)
                    move_along_route!(agent, model, pathfinder)
                    agent.isMoving = true
                    
                    if agent.pos == ingrediente.posicion
                        agent.isMoving = false
                        agent.status = recogeIngrediente
                        println("Cocinero llegó al ingrediente $(comida.tipo_plato)")
                    end
                end
                break
                
            elseif comida.nombre == plato && comida.status == preparando && agent.status == recogeIngrediente
                agent.cont += 1
                if agent.cont >= 3
                    agent.tiene_ingrediente = true
                    agent.status = regresaCocina
                    agent.cont = 0
                    println("Cocinero recogió el ingrediente")
                end
                break
                
            elseif comida.nombre == plato && comida.status == preparando && agent.status == regresaCocina
                plan_route!(agent, agent.posicion_cocina, pathfinder)
                move_along_route!(agent, model, pathfinder)
                agent.isMoving = true
                
                if agent.pos == agent.posicion_cocina
                    agent.isMoving = false
                    agent.status = cocinaOrden
                    println("Cocinero regresó a cocinar")
                end
                break
                
            elseif comida.nombre == plato && comida.status == preparando && agent.status == cocinaOrden
                agent.cont += 1
                if agent.cont >= 15
                    comida.posicion = (11, 11)
                    for comida2 in comidas
                        while comida2.posicion == comida.posicion && comida2 != comida
                            comida.posicion = (comida.posicion[1], comida.posicion[2] + 1)
                        end
                    end
                    comida.status = lista
                    agent.status = recibeOrden 
                    agent.tipo_comida = nothing
                    agent.cont = 0
                    agent.tiene_ingrediente = false
                    println("Cocinero terminó de preparar $(comida.tipo_plato)")
                end
                break
            end
        end
    end
end

function agent_step!(agent::Bartender, model)
    if agent.status == recibeBebida
        if haskey(abmproperties(model), :comidas)
            comidas = abmproperties(model)[:comidas]
            for comida in comidas
                if comida.nombre == bebida && comida.status == orden
                    comida.status = preparando
                    agent.cliente_id = comida.cliente_id
                    agent.status = preparaBebida
                    println("Bartender recibió orden de bebida para cliente $(agent.cliente_id)")
                    break
                end
            end
        end
        
    elseif agent.status == preparaBebida
        agent.cont += 1
        if agent.cont >= 10
            comidas = abmproperties(model)[:comidas]
            comida_idx = findfirst(c -> c.cliente_id == agent.cliente_id && c.nombre == bebida && c.status == preparando, comidas)
            if comida_idx !== nothing
                comidas[comida_idx].status = lista
                comidas[comida_idx].posicion = agent.pos
            end
            agent.status = entregaBebida
            agent.cont = 0
            println("Bartender terminó de preparar la bebida")
        end
        
    elseif agent.status == entregaBebida
        pathfinder = abmproperties(model)[:pathfinder]
        comidas = abmproperties(model)[:comidas]

        comida_idx = findfirst(c -> c.cliente_id == agent.cliente_id && c.nombre == bebida && c.status == lista, comidas)
        if comida_idx === nothing
            return
        end
        comida = comidas[comida_idx]

        for otheragent in allagents(model)
            if otheragent isa Cliente && agent.cliente_id == otheragent.id
                plan_route!(agent, (otheragent.pos[1], otheragent.pos[2] + 1), pathfinder)
                move_along_route!(agent, model, pathfinder)
                agent.isMoving = true
                comida.posicion = agent.pos

                if agent.pos == (otheragent.pos[1], otheragent.pos[2] + 1)
                    agent.isMoving = false
                    agent.status = bebidaEntregada
                    comidas[comida_idx].status = entregada
                    comidas[comida_idx].posicion = otheragent.pos
                    println("Bartender entregó la bebida al cliente $(agent.cliente_id)")
                end
                break
            end
        end
        
    elseif agent.status == bebidaEntregada
        agent.cont += 1
        if agent.cont >= 5
            pathfinder = abmproperties(model)[:pathfinder]
            plan_route!(agent, agent.posicion_barra, pathfinder)
            move_along_route!(agent, model, pathfinder)
            agent.isMoving = true
            
            if agent.pos == agent.posicion_barra
                agent.isMoving = false
                agent.status = recibeBebida
                agent.cliente_id = 0
                agent.cont = 0
                println("Bartender regresó a la barra")
            end
        end
    end
end

function agent_step!(agent::Mesero, model)
    if agent.status == tomaOrden
        if haskey(abmproperties(model), :comidas)
            comidas = abmproperties(model)[:comidas]
            pathfinder = abmproperties(model)[:pathfinder]

            for comida in comidas
                if comida.status == lista && comida.nombre == plato
                    agent.cliente_id = comida.cliente_id
                    plan_route!(agent, (comida.posicion[1] - 1, comida.posicion[2]), pathfinder)
                    move_along_route!(agent, model, pathfinder)
                    agent.isMoving = true
                    if agent.pos == (comida.posicion[1] - 1, comida.posicion[2])
                        agent.isMoving = false
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

        comida_idx = findfirst(c -> c.cliente_id == agent.cliente_id && c.nombre == plato, comidas)
        if comida_idx !== nothing
            comida = comidas[comida_idx]

            for otheragent in allagents(model)
                if otheragent isa Cliente && agent.cliente_id == otheragent.id
                    plan_route!(agent, (otheragent.pos[1], otheragent.pos[2] + 1), pathfinder)
                    move_along_route!(agent, model, pathfinder)
                    agent.isMoving = true
                    comida.posicion = agent.pos

                    if agent.pos == (otheragent.pos[1], otheragent.pos[2] + 1)
                        agent.isMoving = false
                        agent.status = ordenEntregada
                        comidas[comida_idx].status = entregada
                        println("Mesero entregó $(comida.tipo_plato) al cliente $(agent.cliente_id)")
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

function initialize_model()
    space = GridSpace((14,17); periodic=false, metric=:manhattan)
    pathfinder = AStar(space; walkmap=lab, diagonal_movement= false)
    posiciones = [(3,3),(9,13),(12,6)]
    pF = shuffle(posiciones)
    sillas = [
        Silla(false, pF[1], 0),
        Silla(false, pF[2], 0),
        Silla(false, pF[3], 0)
    ]
    ingredientes = [
        Ingredientes(hamburguesa, (5,5)),
        Ingredientes(manzana, (5,7))  
    ]
    properties = Dict(
        :pathfinder => pathfinder, 
        :comidas => Comida[], 
        :sillas => sillas,
        :ingredientes => ingredientes  
    )
    model = StandardABM(Union{Cliente,Mesero,Cocinero,Bartender}, space; agent_step!, properties)

    add_agent!((12,11), Cocinero, model)
    add_agent!((12,14), Bartender, model) 
    add_agent!((5,10), Mesero, model)
    add_agent!((2,14), Cliente, model)
    add_agent!((2,15), Cliente, model)
    add_agent!((2,16), Cliente, model)

    return model, pathfinder
end

model, pathfinder = initialize_model()