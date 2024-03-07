<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Models\UserFile;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class FileController extends Controller
{
    public function upload(Request $request)
    {
        if (!Auth::check()) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }

        $request->validate([
            'pdf' => 'required|mimes:pdf|max:2048',
        ]);

        $user = Auth::user();

        $uploadedFile = $request->file('pdf');
        $originalFilename = $uploadedFile->getClientOriginalName();

        $fileName = $originalFilename;
        $fileCounter = 1;

        while (Storage::disk('local')->exists("public/users-files/user-{$user->id}/$fileName")) {

            $fileName = pathinfo($originalFilename, PATHINFO_FILENAME) . '_' . $fileCounter . '.' . $uploadedFile->getClientOriginalExtension();
            $fileCounter++;
        }

        $path = $uploadedFile->storeAs("public/users-files/user-{$user->id}", $fileName);

        $file = new UserFile(['path' => $path, 'filename' => $fileName]);
        
        $user->files()->save($file);

        return response()->json(['path' => $path, 'filename' => $fileName]);
    }

    public function deleteFile($userId, $fileId)
    {

        $user = Auth::user();
        
        $file = $user->files()->where('id', $fileId)->firstOrFail();

        Storage::delete($file->path);

        $file->delete();

        return response()->json(['message' => 'File deleted successfully']);
    }

    public function getUserFiles()
    {
        $userFiles = Auth::user()->files()->get();

        return response()->json(['files' => $userFiles]);
    }

    public function show($filename)
    {
        $file = Storage::disk('local')->path($filename);
        return response()->file($file);
    }

    public function process()
    {

        $userId = Auth::id();

        $pdfsPath = public_path(). "\storage\users-files\p1\user-" . $userId;

        $pythonScriptPath = app_path(). '/ai/ingest.py';

        $process = new Process(['python3', $pythonScriptPath, $pdfsPath]);

        try {
            // Execute the process
            $process->run();
        
            // Check if the process was not successful
            if (!$process->isSuccessful()) {
                // Throw an exception with the process details
                throw new ProcessFailedException($process);
            } else {
                // Process was successful, you can echo a success message or do something else
                echo "Process executed successfully!";
            }
        } catch (ProcessFailedException $exception) {
            // Echo the error message
            echo "Error: " . $exception->getMessage();
        }
    }

    public function search(Request $request)
    {

        $userId = Auth::id();

        $request->validate([
            'question' => 'required',
        ]);

        $question = $request->input('question');

        $pdfsPath = public_path(). "\storage\users-files\p1\user-" . $userId;

        $pythonScriptPath = app_path(). '/ai/app.py';

        $process = new Process(['python3', $pythonScriptPath, $pdfsPath]);

        try {
            // Execute the process
            $process->run();
        
            // Check if the process was not successful
            if (!$process->isSuccessful()) {
                // Throw an exception with the process details
                throw new ProcessFailedException($process);
            } else {
                // Process was successful, echo the output
                echo "Process executed successfully!<br>";
                // Get and echo the output
                echo "Output: " . $process->getOutput();
            }
        } catch (ProcessFailedException $exception) {
            // Echo the error message
            echo "Error: " . $exception->getMessage();
        }
    }
}