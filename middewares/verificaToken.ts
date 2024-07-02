import jwt from "jsonwebtoken"
import { Request, Response, NextFunction } from 'express'
import { log } from "console"

interface TokenI {
  userLogadoId: number
  userLogadoNome: string
}

export function verificaToken(req: Request | any, res: Response, next: NextFunction) {
  const { authorization } = req.headers

  if (!authorization) {
    res.status(401).json({ error: "Token não informado" })
    return
  }

  try {
    const decode = jwt.verify(authorization, process.env.JWT_KEY as string)
    console.log(decode)
    const { userLogadoId, userLogadoNome } = decode as TokenI

    req.userLogadoId   = userLogadoId
    req.userLogadoNome = userLogadoNome

    next();
  } catch (error) {
    res.status(401).json({ error: "Token inválido" });
  }
}