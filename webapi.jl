include("pacman.jl")
using Genie, Genie.Renderer.Json, Genie.Requests, HTTP
using UUIDs

println(model[1])
println(model[2])
println(model[3])
println(model[4])
println(model[5])

route("/setup") do
    clientes = []
    meseros = []
    cocineros = []
    bartenders = []
    comidas = []
    sillas = []
    ingredientes = []
    for agent in allagents(model)
        if agent isa Cliente
        agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status),
                "isMoving" => agent.isMoving
            )
            push!(clientes, agent_data)
        elseif agent isa Mesero
            agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status),
                "isMoving" => agent.isMoving
            )
            push!(meseros, agent_data)
        elseif agent isa Cocinero 
            agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status),
                "isMoving" => agent.isMoving,
                "tipo_comida" => string(agent.tipo_comida),
                "tiene_ingrediente" => agent.tiene_ingrediente
            )
            push!(cocineros, agent_data)
        elseif agent isa Bartender
            agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status),
                "isMoving" => agent.isMoving
            )
            push!(bartenders, agent_data)
        end
    end
    for comida in abmproperties(model)[:comidas]
        comida_data = Dict(
            "cliente_id" => string(comida.cliente_id),
            "posicion" => [comida.posicion[1], comida.posicion[2]],
            "status" => string(comida.status),
            "nombre" => string(comida.nombre),
            "tipo_plato" => string(comida.tipo_plato)

        )
        push!(comidas, comida_data)
    end
    for silla in abmproperties(model)[:sillas]
        silla_data = Dict(
            "cliente_id" => string(silla.cliente_id),
            "posicion" => [silla.posicion[1], silla.posicion[2]],
            "ocupado" => silla.ocupado
        )
        push!(sillas, silla_data)
    end
    for ingrediente in abmproperties(model)[:ingredientes]
        ingrediente_data = Dict(
            "nombre" => string(ingrediente.nombre),
            "posicion" => [ingrediente.posicion[1], ingrediente.posicion[2]]
        )
        push!(ingredientes, ingrediente_data)
    end

    json(Dict(:msg => "Adios", "cliente" => clientes, "mesero" => meseros, "cocinero" => cocineros, "bartender" => bartenders, "comida" => comidas, "silla" => sillas, "ingrediente" => ingredientes))
end

route("/run") do
    run!(model, 1)
    sleep(0.2)
    clientes = []
    meseros = []
    cocineros = []
    bartenders = []
    comidas = []
    sillas = []
    ingredientes = []
    for agent in allagents(model)
        if agent isa Cliente
        agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status),
                "isMoving" => agent.isMoving
            )
            push!(clientes, agent_data)
        elseif agent isa Mesero
            agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status),
                "isMoving" => agent.isMoving
            )
            push!(meseros, agent_data)
        elseif agent isa Cocinero 
            agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status),
                "isMoving" => agent.isMoving,
                "tipo_comida" => string(agent.tipo_comida),
                "tiene_ingrediente" => agent.tiene_ingrediente
            )
            push!(cocineros, agent_data)
        elseif agent isa Bartender
            agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status),
                "isMoving" => agent.isMoving
            )
            push!(bartenders, agent_data)
        end
    end
    for comida in abmproperties(model)[:comidas]
        comida_data = Dict(
            "cliente_id" => string(comida.cliente_id),
            "posicion" => [comida.posicion[1], comida.posicion[2]],
            "status" => string(comida.status),
            "nombre" => string(comida.nombre),
            "tipo_plato" => string(comida.tipo_plato)
        )
        push!(comidas, comida_data)
    end
    for silla in abmproperties(model)[:sillas]
        silla_data = Dict(
            "cliente_id" => string(silla.cliente_id),
            "posicion" => [silla.posicion[1], silla.posicion[2]],
            "ocupado" => silla.ocupado
        )
        push!(sillas, silla_data)
    end
    for ingrediente in abmproperties(model)[:ingredientes]
        ingrediente_data = Dict(
            "nombre" => string(ingrediente.nombre),
            "posicion" => [ingrediente.posicion[1], ingrediente.posicion[2]]
        )
        push!(ingredientes, ingrediente_data)
    end
    json(Dict(:msg => "Adios", "cliente" => clientes, "mesero" => meseros, "cocinero" => cocineros, "bartender" => bartenders, "comida" => comidas, "silla" => sillas, "ingrediente" => ingredientes))
end

Genie.config.run_as_server = true
Genie.config.cors_headers["Access-Control-Allow-Origin"] = "*"
Genie.config.cors_headers["Access-Control-Allow-Headers"] = "Content-Type"
Genie.config.cors_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
Genie.config.cors_allowed_origins = ["*"]

up()