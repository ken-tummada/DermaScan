//
//  CameraView.swift
//  DermaScan
//
//  Created by Zihan on 2025/3/4.
//

import SwiftUI
import UIKit

struct CameraView: UIViewControllerRepresentable {
    @Binding var isPresented: Bool
    var onImageCaptured: (UIImage) -> Void

    class Coordinator: NSObject, UINavigationControllerDelegate, UIImagePickerControllerDelegate {
        var parent: CameraView

        init(parent: CameraView) {
            self.parent = parent
        }

        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey: Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.onImageCaptured(image)
            }
            parent.isPresented = false
        }

        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.isPresented = false
        }
    }

    func makeCoordinator() -> Coordinator {
        return Coordinator(parent: self)
    }

    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.sourceType = .camera
        picker.cameraCaptureMode = .photo
        picker.mediaTypes = ["public.image"]
        picker.delegate = context.coordinator
        
        picker.modalPresentationStyle = .fullScreen
        picker.view.clipsToBounds = true
        return picker
    }

    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}
}
