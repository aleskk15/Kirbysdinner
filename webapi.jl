include("pacman.jl")
using Genie, Genie.Renderer.Json, Genie.Requests, HTTP
using UUIDs

route("/setup") do
    clientes = []
    meseros = []
    cocineros = []
    comidas = []
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
                "isMoving" => agent.isMoving
            )
            push!(cocineros, agent_data)
        end
    end
    for comida in abmproperties(model)[:comidas]
        comida_data = Dict(
            "cliente_id" => string(comida.cliente_id),
            "posicion" => [comida.posicion[1], comida.posicion[2]],
            "status" => string(comida.status)
        )
        push!(comidas, comida_data)
    end
    json(Dict(:msg => "Adios", "cliente" => clientes, "mesero" => meseros, "cocinero" => cocineros, "comida" => comidas))
end

route("/run") do
    run!(model, 1)
    clientes = []
    meseros = []
    cocineros = []
    comidas = []
    for agent in allagents(model)
        if agent isa Cliente
        agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status)
            )
            push!(clientes, agent_data)
        elseif agent isa Mesero
            agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status)
            )
            push!(meseros, agent_data)
        elseif agent isa Cocinero 
            agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]],
                "status" => string(agent.status)
            )
            push!(cocineros, agent_data)
        end
    end
    for comida in abmproperties(model)[:comidas]
        comida_data = Dict(
            "cliente_id" => string(comida.cliente_id),
            "posicion" => [comida.posicion[1], comida.posicion[2]],
            "status" => string(comida.status),
            "nombre" => string(comida.nombre)
        )
        push!(comidas, comida_data)
    end
    json(Dict(:msg => "Adios", "cliente" => clientes, "mesero" => meseros, "cocinero" => cocineros, "comida" => comidas))
end

Genie.config.run_as_server = true
Genie.config.cors_headers["Access-Control-Allow-Origin"] = "*"
Genie.config.cors_headers["Access-Control-Allow-Headers"] = "Content-Type"
Genie.config.cors_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
Genie.config.cors_allowed_origins = ["*"]

up()