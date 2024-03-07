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
    public function upload_and_ingest(Request $request)
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

        $userId = Auth::id();

        $filePath = public_path(). "\storage\users-files\user-" . $userId;

        $pythonScriptPath = app_path(). '/ai/ingest.py';

        $process = new Process(['python3', $pythonScriptPath, $filePath, $userId]);

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

        // return response()->json(['path' => $path, 'filename' => $fileName]);
    }

    public function deleteFile($userId, $fileId)
    {

        $user = Auth::user();

        $userId = Auth::id();
        
        $file = $user->files()->where('id', $fileId)->firstOrFail();

        Storage::delete($file->path);

        function deleteDirectory($directory) {
            if (!is_dir($directory)) {
                return false;
            }
        
            $files = scandir($directory);
            foreach ($files as $file) {
                if ($file !== '.' && $file !== '..') {
                    $path = $directory . '/' . $file;
                    if (is_dir($path)) {
                        // Recursively delete subdirectories
                        deleteDirectory($path);
                    } else {
                        // Delete files
                        unlink($path);
                    }
                }
            }
        
            // Delete the directory itself
            return rmdir($directory);
        }
        
        $directoryToDelete = app_path(). '/ai/DB/user-' . $userId;

        $result = deleteDirectory($directoryToDelete);

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

    public function search(Request $request)
    {

        $userId = Auth::id();

        $request->validate([
            'question' => 'required',
        ]);

        $question = $request->input('question');

        $pythonScriptPath = app_path(). '/ai/app.py';

        $process = new Process(['python3', $pythonScriptPath, $question, $userId]);

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