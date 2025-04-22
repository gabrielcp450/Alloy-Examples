#!/usr/bin/env python3
"""
Script para gerar visualizações dos exemplos Alloy.
Este script executa os modelos Alloy e gera imagens representativas da visualização.
"""

import os
import subprocess
import sys
from pathlib import Path

# Paths
CURRENT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = CURRENT_DIR.parent
ALLOY_JAR = CURRENT_DIR / "org.alloytools.alloy.dist.jar"
SPECS_DIR = PROJECT_ROOT / "specifications"
IMG_DIR = PROJECT_ROOT / "img"

def compile_viz_generator():
    """Compile the Java visualization generator."""
    try:
        subprocess.run([
            "javac", 
            "-cp", str(ALLOY_JAR), 
            str(CURRENT_DIR / "AlloyRunnerWithViz.java")
        ], check=True)
        print("Compiled AlloyRunnerWithViz.java successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error compiling AlloyRunnerWithViz.java: {e}")
        return False

def generate_visualization(als_file, output_image):
    """Generate visualization for an Alloy model."""
    try:
        subprocess.run([
            "java", 
            "-cp", f"{ALLOY_JAR}:{CURRENT_DIR}", 
            "AlloyRunnerWithViz",
            str(als_file),
            str(output_image)
        ], check=True)
        print(f"Generated visualization: {output_image}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating visualization for {als_file}: {e}")
        return False

def generate_all_visualizations():
    """Generate visualizations for all example models."""
    # Ensure output directory exists
    os.makedirs(IMG_DIR, exist_ok=True)
    
    # Make sure the visualization generator is compiled
    if not compile_viz_generator():
        return
    
    # Teaching Concurrency example
    tc_model = SPECS_DIR / "TeachingConcurrency" / "Simple.als"
    tc_output = IMG_DIR / "teaching_concurrency_run.png"
    
    if tc_model.exists():
        generate_visualization(tc_model, tc_output)
    else:
        print(f"Model file not found: {tc_model}")
    
    # Echo algorithm example
    echo_model = SPECS_DIR / "echo" / "Echo.als"
    echo_output = IMG_DIR / "echo_run.png"
    
    if echo_model.exists():
        generate_visualization(echo_model, echo_output)
    else:
        print(f"Model file not found: {echo_model}")

    # Create dummy files if the above fails
    if not tc_output.exists():
        create_dummy_image(tc_output, "Teaching Concurrency")
    
    if not echo_output.exists():
        create_dummy_image(echo_output, "Echo Algorithm")

def create_dummy_image(output_path, title):
    """Create a dummy image in case visualization fails."""
    try:
        script = f'''
        import java.awt.image.BufferedImage;
        import java.awt.Graphics2D;
        import java.awt.Color;
        import java.io.File;
        import javax.imageio.ImageIO;
        
        public class CreateDummyImage {{
            public static void main(String[] args) throws Exception {{
                int width = 800;
                int height = 600;
                BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
                Graphics2D g2d = image.createGraphics();
                
                g2d.setColor(Color.WHITE);
                g2d.fillRect(0, 0, width, height);
                
                g2d.setColor(Color.BLACK);
                g2d.drawString("Alloy Visualization for: {title}", 50, 50);
                g2d.drawString("This is a placeholder image", 50, 80);
                
                ImageIO.write(image, "png", new File("{output_path}"));
                g2d.dispose();
            }}
        }}
        '''
        
        # Write the Java file
        dummy_java = CURRENT_DIR / "CreateDummyImage.java"
        with open(dummy_java, 'w') as f:
            f.write(script)
        
        # Compile and run
        subprocess.run(["javac", str(dummy_java)], check=True)
        subprocess.run(["java", "-cp", str(CURRENT_DIR), "CreateDummyImage"], check=True)
        
        print(f"Created dummy image: {output_path}")
        
        # Clean up
        os.unlink(dummy_java)
        os.unlink(CURRENT_DIR / "CreateDummyImage.class")
        
    except Exception as e:
        print(f"Error creating dummy image: {e}")

if __name__ == "__main__":
    generate_all_visualizations()
    print("Visualization generation complete") 