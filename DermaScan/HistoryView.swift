//
//  HistoryView.swift
//  DermaScan
//
//  Created by Zihan on 2025/3/4.
//

import SwiftUI

struct HistoryView: View {
    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        ZStack {
            // 底层黑色背景
            Color.black.ignoresSafeArea()
            
            // 叠加渐变层
            LinearGradient(gradient: Gradient(colors: [
                Color(hex: "0D7377").opacity(0.6),
                Color(hex: "0D7377").opacity(0.0)
            ]), startPoint: .top, endPoint: .bottom)
            .ignoresSafeArea()
            
            VStack {
                HStack {
                    Button(action: {
                        presentationMode.wrappedValue.dismiss()
                    }) {
                        Image(systemName: "chevron.left")
                            .foregroundColor(.white)
                            .font(.system(size: 20, weight: .bold))
                            .padding()
                    }
                    Spacer()
                }
                Spacer()
            }
        }
    }
}

#Preview {
    HistoryView()
}
