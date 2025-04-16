import java.io.File;
import java.io.IOException;
import java.util.Optional;

import edu.mit.csail.sdg.alloy4whole.ExampleUsingTheCompiler;
import edu.mit.csail.sdg.alloy4.Err;
import edu.mit.csail.sdg.parser.CompModule;
import edu.mit.csail.sdg.parser.CompUtil;
import edu.mit.csail.sdg.ast.Func;
import edu.mit.csail.sdg.ast.Command;
import edu.mit.csail.sdg.sim.SimInstance;
import edu.mit.csail.sdg.translator.TranslateAlloyToKodkod;
import edu.mit.csail.sdg.translator.A4Options;
import edu.mit.csail.sdg.translator.A4Options.SatSolver;
import edu.mit.csail.sdg.translator.A4Solution;
import edu.mit.csail.sdg.alloy4.A4Reporter;
import kodkod.engine.satlab.SATFactory;
import static edu.mit.csail.sdg.alloy4.A4Preferences.Solver;
import edu.mit.csail.sdg.alloy4.A4Preferences.ChoicePref;
import edu.mit.csail.sdg.alloy4.WorkerEngine;

public class AlloyRunner {
    public static void main(String[] args) {
        try {
            
            // Load Alloy model
            File alloyFile = new File("learning_conc.als");
            A4Reporter rep = new A4Reporter();

            // Parse the model
            CompModule world = CompUtil.parseEverything_fromFile(null, null, alloyFile.getAbsolutePath());

            // Options for the solver
            A4Options options = new A4Options();
            //System.out.println(A4Options.SatSolver.values());
            options.solver = A4Options.SatSolver.parse("nuXmv");
            //A4Options.SatSolver.make("nuXmv", "nuXmv", "./nuXmv");
            
            // Run all commands in the model
            Command command = world.getAllCommands().get(world.getAllCommands().size() - 1);
            System.out.println("Executing command: " + command.label);
            
            // Start timing
            A4Solution solution = TranslateAlloyToKodkod.execute_command(rep, world.getAllReachableSigs(), command, options);
            solution = TranslateAlloyToKodkod.execute_command(rep, world.getAllReachableSigs(), command, options);
            solution = TranslateAlloyToKodkod.execute_command(rep, world.getAllReachableSigs(), command, options);
            solution = TranslateAlloyToKodkod.execute_command(rep, world.getAllReachableSigs(), command, options);
            long startTime = System.currentTimeMillis();
            solution = TranslateAlloyToKodkod.execute_command(rep, world.getAllReachableSigs(), command, options);
            // End timing
            long endTime = System.currentTimeMillis();
            
            // Calculate elapsed time
            long elapsedTime = endTime - startTime;

            // Output elapsed time
            System.out.println("Finished in " + elapsedTime + "ms");

            // Output whether solution is satisfiable
            if (solution.satisfiable()) {
                System.out.println("Instance found. Predicate is consistent.");
            } else {
                System.out.println("No counterexample found. Assertion may be valid.");
            }

        } catch (Err err) {
            err.printStackTrace();
        }
    }
}
