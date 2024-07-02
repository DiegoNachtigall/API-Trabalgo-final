import express from 'express'
const app = express()
// const port = 3000
const port = process.env.PORT ?? 3000

import UsuariosRoutes from './routes/usuarios'
import JogosRoutes from './routes/jogos'
import LoginRoutes from './routes/login'

app.use(express.json())
app.use("/Usuarios", UsuariosRoutes)
app.use("/Jogos", JogosRoutes)
app.use("/Login", LoginRoutes)

app.get('/', (req, res) => {
  res.send('API de ')
})

app.listen(port, () => {
  console.log(`Servidor rodando na porta: http://localhost:${port}`)
})