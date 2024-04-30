<?php

namespace App\Http\Controllers\API\v1;

use Illuminate\Http\Request;
use App\Models\User;
use App\HTTP\Controllers\Controller;

class APIController extends Controller
{
    public function index($userId)
    {
        $user = User::findOrFail($userId);

        $filenames = $user->files()->pluck('filename')->toArray();

        return response()->json(['filenames' => $filenames]);
    }

    public function search($userId, $question)
    {
        ini_set('max_execution_time', 12000);

        dd($userId, $question);

        $history = $request->input('history');

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