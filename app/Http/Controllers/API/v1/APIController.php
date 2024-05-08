<?php

namespace App\Http\Controllers\API\v1;

use Illuminate\Http\Request;
use App\Models\User;
use App\Http\Controllers\Controller;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Illuminate\Support\Facades\Validator;

class APIController extends Controller
{
    public function index($userId)
    {
        $user = User::findOrFail($userId);

        $filenames = $user->files()->pluck('filename')->toArray();

        return response()->json(['filenames' => $filenames]);
    }

    public function refresh_dialog (Request $request) {
        $user = $request->user();
    
        // Ensure the user is authenticated
        if (!$user) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }
    
        // Return the generated token
        return ['token' => $user->api_token];
    }

    public function get_token (Request $request) {
        $user = $request->user();
    
        // Ensure the user is authenticated
        if (!$user) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }
    
        // Return the generated token
        return ['token' => $user->api_token];
    }

    public function search($userId, Request $request)
    {
        ini_set('max_execution_time', 12000);

        $question = $request->input('question');

        $history = $request->input('question');

        $initial_prompt = $request->input('initialPrompt');

        $pythonScriptPath = app_path(). '/ai/app.py';

        $process = new Process(['python3', $pythonScriptPath, $question, $userId, $initial_prompt, $history]);

        try {
            // Execute the process
            $process->run();
        
            // Check if the process was not successful
            if (!$process->isSuccessful()) {
                // Throw an exception with the process details
                throw new ProcessFailedException($process);
            } else {
                // Get and echo the output
                echo $process->getOutput();
            }
        } catch (ProcessFailedException $exception) {
            // Echo the error message
            echo "Error: " . $exception->getMessage();
        }
    }

}