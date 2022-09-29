using System;
using Microsoft.SolverFoundation;
using Microsoft.SolverFoundation.Common;
using Microsoft.SolverFoundation.Services;

namespace OpdrachtKlein
{
    class Program
    {
        static void Main(string[] args)
        {
            // Set up solver
            SolverContext context = SolverContext.GetContext();
            Model model = context.CreateModel();
            
            // Preprocessing should give arrays with the lengths of the images
            // as well as the lengths of the blocks (in the order that they appear)
            // length of last block should be sufficiently big to fit all images
            int[] blocks = new int[] { 11, 6, 6, 99};
            int[] images = new int[] { 10, 3, 4, 4 };
            Decision[] imageInBlock = new Decision[blocks.Length * images.Length];
            for (int i = 0; i < images.Length; i++)
            {
                for (int j = 0; j < blocks.Length; j++)
                {
                    imageInBlock[i * blocks.Length + j] = new Decision(Domain.Boolean, $"x{i}_{j}");
                }
            }
            model.AddDecisions(imageInBlock);
            // No block exceeds its limit
            for (int j = 0; j < blocks.Length; j++)
            {
                Term r = 0;
                for (int i = 0; i < images.Length; i++)
                {
                    r += images[i] * imageInBlock[i * blocks.Length + j];
                }
                model.AddConstraint($"capacity{j}", r <= blocks[j]);
            }
            // Every image is in exactly 1 block
            for (int i = 0; i < images.Length; i++)
            {
                Term r = 0;
                for (int j = 0; j < blocks.Length; j++)
                {
                    r += imageInBlock[i * blocks.Length + j];
                }
                model.AddConstraint($"allSent{i}", r == 1);
            }

            // Potential function
            Term Goal()
            {
                Term res = 0;
                for (int i = 0; i < images.Length; i++)
                {
                    for (int j = 0; j < blocks.Length; j++)
                    {
                        // This starts at index 0 but that shouldn't matter
                        res += images[i] * j * imageInBlock[i * blocks.Length + j];
                    }
                }
                return res;
            }
            model.AddGoal("penaltyFunc", GoalKind.Minimize, Goal());
            
            // Solve
            Solution solution = context.Solve(new MixedIntegerProgrammingDirective());
            Console.Write(solution.GetReport());

            Console.ReadLine();
        }
    }
}
