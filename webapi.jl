include("pacman.jl")
using Genie, Genie.Renderer.Json, Genie.Requests, HTTP
using UUIDs

route("/setup") do
    clientes = []
    meseros = []
    cocineros = []
    for agent in allagents(model)
        if agent isa Cliente
        agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]] 
            )
            push!(clientes, agent_data)
        elseif agent isa Mesero
            agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]] 
            )
            push!(meseros, agent_data)
        elseif agent isa Cocinero 
            agent_data = Dict(
                "id" => string(agent.id),  
                "pos" => [agent.pos[1], agent.pos[2]] 
            )
            push!(cocineros, agent_data)
        end
    end
    json(Dict(:msg => "Adios", "cliente" => clientes, "mesero" => meseros, "cocinero" => cocineros))
end

route("/run") do
    run!(model, 1)
    clientes = []
    meseros = []
    cocineros = []
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
    json(Dict(:msg => "Adios", "cliente" => clientes, "mesero" => meseros, "cocinero" => cocineros))
end

Genie.config.run_as_server = true
Genie.config.cors_headers["Access-Control-Allow-Origin"] = "*"
Genie.config.cors_headers["Access-Control-Allow-Headers"] = "Content-Type"
Genie.config.cors_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
Genie.config.cors_allowed_origins = ["*"]

up()