import { PrismaClient } from "@prisma/client";
import { Router } from "express";

import { verificaToken } from "../middewares/verificaToken";

const prisma = new PrismaClient();

async function main() {
  /***********************************/
  /* SOFT DELETE MIDDLEWARE */
  /***********************************/
  prisma.$use(async (params, next) => {
    // Check incoming query type
    if (params.model == "Jogo") {
      if (params.action == "delete") {
        // Delete queries
        // Change action to an update
        params.action = "update";
        params.args["data"] = { deleted: true };
      }
    }
    return next(params);
  });
}
main();

const router = Router();

// CRUD
// Read
router.get("/", async (req: any, res) => {

    const jogos = await prisma.jogo.findMany({
      where: { deleted: false },
    });
    res.status(200).json(jogos);
  
});

// Create
router.post("/", verificaToken, async (req: any, res) => {
  const { nome, descricao, preco, genero } = req.body;

  const { userLogadoId } = req;

  if (!nome || !descricao || !preco || !genero) {
    res.status(400).json({ erro: "Informe todos os dados" });
    return;
  }

  try {
    const jogo = await prisma.jogo.create({
      data: { nome, descricao, preco, genero, usuarioId: userLogadoId },
    });
    res.status(201).json(jogo);
  } catch (error) {
    res.status(400).json(error);
  }
});

// Delete
router.delete("/:id", verificaToken, async (req, res) => {
  const { id } = req.params;

  try {
    const jogos = await prisma.jogo.delete({
      where: { id: Number(id) },
    });
    res.status(200).json(jogos);
  } catch (error) {
    res.status(400).json(error);
  }
});

router.put("/:id", verificaToken, async (req, res) => {
  const { id } = req.params;
  const { preco } = req.body;

  if (!preco) {
    res.status(400).json({ erro: "Informe o preço" });
    return;
  }

  try {
    const jogos = await prisma.jogo.update({
      where: { id: Number(id) },
      data: { preco },
    });
    res.status(200).json(jogos);
  } catch (error) {
    res.status(400).json(error);
  }
});

export default router;
