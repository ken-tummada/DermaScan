//
//  RecordsView.swift
//  DermaScan
//
//  Created by Zihan on 2025/3/4.
//

import SwiftUI

struct RecordsView: View {
    var body: some View {
        ZStack {
            Color(hex: "303134")
                .ignoresSafeArea()
            
            VStack {
                ZStack {
                    Text("Records")
                        .foregroundColor(.white)
                        .font(.system(size: 23, weight: .semibold))
                    
                    HStack {
                        Spacer()
                        
                        Button(action: {
                            // To Clean All History Data
                        }) {
                            ZStack {
                                Circle()
                                    .frame(width: 35, height: 35)
                                    .foregroundColor(Color.black.opacity(0.3))
                                Image("clear")
                                    .resizable()
                                    .scaledToFit()
                                    .frame(height: 22)
                                    .foregroundColor(.white.opacity(0.8))
                            }
                        }
                        .buttonStyle(.borderless)
                    }
                }
                .padding(.horizontal, 32)
                
                Spacer()
            }
            .padding(.top, 25)
        }
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
    }
}

#Preview {
    RecordsView()
}
